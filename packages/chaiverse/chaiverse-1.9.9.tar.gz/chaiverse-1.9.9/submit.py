import itertools
import sys

import time

from chaiverse import utils
from chaiverse.login_cli import auto_authenticate
from chaiverse.http_client import SubmitterClient
from chaiverse import config

if 'ipykernel' in sys.modules:
    from IPython.core.display import display


class ModelSubmitter:
    """
    Submits a model to the Guanaco service and exposes it to beta-testers on the Chai app.

    Attributes
    --------------
    developer_key : str
    verbose       : str - Print deployment logs

    Methods
    --------------
    submit(submission_params)
    Submits the model to the Guanaco service.

    Example usage:
    --------------
    submitter = ModelSubmitter(developer_key)
    submitter.submit(submission_params)
    """

    @auto_authenticate
    def __init__(self, developer_key=None, verbose=False):
        self.developer_key = developer_key
        self.verbose = verbose
        self._animation = self._spinner_animation_generator()
        self._progress = 0
        self._sleep_time = 0.5
        self._get_request_interval = int(10 / self._sleep_time)
        self._logs_cache = []

    def submit(self, submission_params):
        """
        Submits the model to the Guanaco service and wait for the deployment to finish.

        submission_params: dict
            model_repo: str - HuggingFace repo
            hf_auth_token (optional): str - A read-only token used to access model_repo
            generation_params: dict
                temperature: float
                top_p: float
                top_k: int
                repetition_penalty: float
            formatter (optional): PromptFormatter
            reward_formatter (optional): PromptFormatter
            model_name (optional): str - custom alias for your model
        """
        submission_params = submission_params.copy()
        submission_params = self._preprocess_submission(submission_params)
        return self._handle_submit(submit_model, submission_params)

    def _preprocess_submission(self, submission_params):
        if submission_params.get('formatter'):
            submission_params["formatter"] = submission_params["formatter"].dict()
        if submission_params.get("reward_formatter"):
            submission_params["reward_formatter"] = submission_params["reward_formatter"].dict()
        return submission_params

    def submit_blend(self, submission_params):
        """
        Submits blend to the Guanaco service and wait for the deployment to finish.

        submission_params: dict
            submissions: list - submission_ids for the models in the blend
            model_name (optional): str - custom alias for your model
        """
        return self._handle_submit(submit_model_blend, submission_params)

    def _handle_submit(self, submission_func, submission_params):
        check_user_accepts_eula()
        submission_response = submission_func(submission_params, self.developer_key)
        submission_id = submission_response.get('submission_id')
        self._print_submission_header(submission_id)
        status = self._wait_for_model_submission(submission_id)
        self._print_submission_result(status)
        self._progress = 0
        return submission_id

    def _wait_for_model_submission(self, submission_id):
        status = 'pending'
        while status not in {'deployed', 'failed', 'inactive'}:
            status = self._get_submission_status(submission_id)
            self._display_animation(status)
            time.sleep(self._sleep_time)
        return status

    def _get_submission_status(self, submission_id):
        self._progress += 1
        status = 'pending'
        if self._progress % self._get_request_interval == 0:
            model_info = get_model_info(submission_id, self.developer_key)
            self._print_latest_logs(model_info)
            status = model_info.get('status')
        return status

    def _spinner_animation_generator(self):
        animations = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
        return itertools.cycle(animations)

    def _display_animation(self, status):
        text = f" {next(self._animation)} {status}..."
        if 'ipykernel' in sys.modules:
            display(text, display_id="animation")
        else:
            print(text, end='\r')

    def _print_submission_header(self, submission_id):
        utils.print_color(f'\nModel Submission ID: {submission_id}', 'green')
        print("Your model is being deployed to Chaiverse, please wait for approximately 10 minutes...")

    def _print_submission_result(self, status):
        success = status == 'deployed'
        text_success = 'Model successfully deployed!'
        text_failed = 'Model deployment failed, please seek help on our Discord channel'
        text = text_success if success else text_failed
        color = 'green' if success else 'red'
        print('\n')
        utils.print_color(f'\n{text}', color)

    def _print_latest_logs(self, model_info):
        if self.verbose:
            logs = model_info.get("logs", [])
            num_new_logs = len(logs) - len(self._logs_cache)
            new_logs = logs[-num_new_logs:] if num_new_logs else []
            self._logs_cache += new_logs
            for log in new_logs:
                message = utils.parse_log_entry(log)
                print(message)


@auto_authenticate
def submit_model(model_submission: dict, developer_key=None):
    http_client = SubmitterClient(developer_key)
    response = http_client.post(endpoint=config.SUBMISSION_ENDPOINT, data=model_submission)
    return response


@auto_authenticate
def submit_model_blend(model_submission: dict, developer_key=None):
    http_client = SubmitterClient(developer_key)
    response = http_client.post(endpoint=config.BLEND_SUBMISSION_ENDPOINT, data=model_submission)
    return response


@auto_authenticate
def get_model_info(submission_id, developer_key=None):
    http_client = SubmitterClient(developer_key)
    response = http_client.get(endpoint=config.INFO_ENDPOINT, submission_id=submission_id)
    return response


@auto_authenticate
def evaluate_model(submission_id, developer_key=None):
    http_client = SubmitterClient(developer_key)
    response = http_client.get(endpoint=config.EVALUATE_ENDPOINT, submission_id=submission_id)
    return response


@auto_authenticate
def get_my_submissions(developer_key=None):
    http_client = SubmitterClient(developer_key)
    response = http_client.get(endpoint=config.ALL_SUBMISSION_STATUS_ENDPOINT)
    return response


@auto_authenticate
def deactivate_model(submission_id, developer_key=None):
    http_client = SubmitterClient(developer_key)
    response = http_client.get(endpoint=config.DEACTIVATE_ENDPOINT,submission_id=submission_id)
    print(response)
    return response


@auto_authenticate
def redeploy_model(submission_id, developer_key=None):
    http_client = SubmitterClient(developer_key)
    response = http_client.get(endpoint=config.REDEPLOY_ENDPOINT, submission_id=submission_id)
    print(response)
    return response


@auto_authenticate
def teardown_model(submission_id, developer_key=None):
    http_client = SubmitterClient(developer_key)
    response = http_client.get(endpoint=config.TEARDOWN_ENDPOINT, submission_id=submission_id)
    print(response)
    return response


@auto_authenticate
def check_user_accepts_eula(developer_key):
    text = "Thank you! Before submitting a model, please acknowledge that you have"\
           " read our End-user license agreement (EULA),"\
           "\nwhich can be found at: www.chai-research.com/competition-eula.html 🥳."\
           "\nPlease type 'accept' to confirm that you have read and agree with our EULA: "
    input_text = input(text)
    if input_text.lower().strip() != 'accept':
        raise ValueError('In order to submit a model, you must agree with our EULA 😢')

