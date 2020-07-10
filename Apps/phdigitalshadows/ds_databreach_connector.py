#
# Copyright (c) 2019 Digital Shadows Ltd.
#
import phantom.app as phantom
from phantom.action_result import ActionResult

from digital_shadows_consts import DS_API_KEY_CFG, DS_API_SECRET_KEY_CFG
from digital_shadows_consts import DS_GET_BREACH_SUCCESS, DS_GET_BREACH_NOT_FOUND

from dsapi.service.data_breach_service import DataBreachService
from dsapi.service.data_breach_record_service import DataBreachRecordService


class DSDataBreachConnector(object):

    def __init__(self, connector):
        """
        :param connector: DigitalShadowsConnector
        """
        self._connector = connector

        config = connector.get_config()
        self._ds_api_key = config[DS_API_KEY_CFG]
        self._ds_api_secret_key = config[DS_API_SECRET_KEY_CFG]

    def get_data_breach_by_id(self, param):
        action_result = ActionResult(dict(param))
        self._connector.add_action_result(action_result)
        breach_service = DataBreachService(self._ds_api_key, self._ds_api_secret_key)
        breach = breach_service.find_data_breach_by_id(param['breach_id'])

        if 'id' in breach:
            summary = {
                'data_breach_count': 1,
                'data_breach_found': True
            }
            action_result.update_summary(summary)
            action_result.add_data(breach)
            action_result.set_status(phantom.APP_SUCCESS, DS_GET_BREACH_SUCCESS)
        else:
            summary = {
                'data_breach_count': 0,
                'data_breach_found': False
            }
            action_result.update_summary(summary)
            action_result.set_status(phantom.APP_SUCCESS, DS_GET_BREACH_NOT_FOUND)
        return action_result.get_status()

    def get_data_breach(self, param):
        action_result = ActionResult(dict(param))
        self._connector.add_action_result(action_result)

        date_range = str(param['date_range'])
        param_reposted_credentials = None if 'reposted_credentials' not in param else param['reposted_credentials'].split(',')
        param_severities = None if 'severities' not in param else param.get('severities').split(',')
        param_statuses = None if 'statuses' not in param else param.get('statuses').split(',')
        param_user_name = None if 'user_name' not in param else param.get('user_name').split(',')

        breach_service = DataBreachService(self._ds_api_key, self._ds_api_secret_key)
        breach_view = DataBreachService.data_breach_view(published=date_range, reposted_credentials=param_reposted_credentials,
                                                         severities=param_severities, statuses=param_statuses, username=param_user_name)

        breach_pages = breach_service.find_all_pages(view=breach_view)

        breach_total = len(breach_pages)
        if breach_total > 0:
            summary = {
                'data_breach_count': breach_total,
                'data_breach_found': True
            }
            action_result.update_summary(summary)

            for breach_page in breach_pages:
                for breach in breach_page:
                    # self._connector.save_progress('breach: ' + str(breach))
                    action_result.add_data(breach.payload)
            action_result.set_status(phantom.APP_SUCCESS, DS_GET_BREACH_SUCCESS)
        else:
            summary = {
                'data_breach_count': 0,
                'data_breach_found': False
            }
            action_result.update_summary(summary)
            action_result.set_status(phantom.APP_SUCCESS, DS_GET_BREACH_NOT_FOUND)
        return action_result.get_status()

    def get_data_breach_record(self, param):
        action_result = ActionResult(dict(param))
        self._connector.add_action_result(action_result)

        date_range = str(param['date_range'])
        if 'domain_names' in param:
            param_domain_names = param['domain_names'].split(',')
        else:
            param_domain_names = None

        if 'review_statuses' in param:
            param_review_statuses = param['review_statuses'].split(',')
        else:
            param_review_statuses = None

        param_distinction = None if 'distinction' not in param else str(param.get('distinction'))
        param_user_name = None if 'user_name' not in param else str(param.get('user_name'))
        param_password = None if 'password' not in param else str(param.get('password'))

        breach_record_service = DataBreachRecordService(self._ds_api_key, self._ds_api_secret_key)
        breach_record_view = DataBreachRecordService.data_breach_records_view(published=date_range, domain_names=param_domain_names, username=param_user_name,
                                                         password=param_password, review_statuses=param_review_statuses, distinction=param_distinction)
        self._connector.save_progress(str(breach_record_view))
        breach_record_pages = breach_record_service.read_all_records(view=breach_record_view)

        breach_record_total = len(breach_record_pages)
        if breach_record_total > 0:
            summary = {
                'data_breach_record_count': breach_record_total,
                'data_breach_record_found': True
            }
            action_result.update_summary(summary)
            for breach_record_page in breach_record_pages:
                for breach_record in breach_record_page:
                    action_result.add_data(breach_record.payload)
            action_result.set_status(phantom.APP_SUCCESS, "Digital Shadows data breach records fetched")
        else:
            summary = {
                'data_breach_record_count': 0,
                'data_breach_record_found': False
            }
            action_result.update_summary(summary)
            action_result.set_status(phantom.APP_SUCCESS, "Data breach record not found in Digital Shadows")
        return action_result.get_status()

    def get_data_breach_record_by_id(self, param):
        action_result = ActionResult(dict(param))
        self._connector.add_action_result(action_result)
        breach_record_service = DataBreachRecordService(self._ds_api_key, self._ds_api_secret_key)
        breach_record_pages = breach_record_service.find_all_pages(param['breach_id'])

        breach_record_total = len(breach_record_pages)
        if breach_record_total > 0:
            summary = {
                'data_breach_record_count': breach_record_total,
                'data_breach_record_found': True
            }
            action_result.update_summary(summary)
            for breach_record_page in breach_record_pages:
                for breach_record in breach_record_page:
                    action_result.add_data(breach_record.payload)
            action_result.set_status(phantom.APP_SUCCESS, "Digital Shadows data breach records fetched")
        else:
            summary = {
                'data_breach_record_count': 0,
                'data_breach_record_found': False
            }
            action_result.update_summary(summary)
            action_result.set_status(phantom.APP_SUCCESS, "Data breach record not found in Digital Shadows")
        return action_result.get_status()

    def get_data_breach_record_by_username(self, param):
        action_result = ActionResult(dict(param))
        self._connector.add_action_result(action_result)
        breach_record_service = DataBreachRecordService(self._ds_api_key, self._ds_api_secret_key)

        user_name = str(param['user_name'])
        domain_names_param = None if 'domain_names' not in param else param['domain_names'].split(',')
        review_statuses_param = None if 'review_statuses' not in param else param['review_statuses'].split(',')
        published_date_range = 'ALL' if 'published_date_range' not in param else str(param['published_date_range'])

        breach_record_view = DataBreachRecordService.data_breach_records_view(username=user_name, published=published_date_range,
                                                             domain_names=domain_names_param, review_statuses=review_statuses_param)
        self._connector.save_progress("Breach record View: " + str(breach_record_view))
        breach_record_pages = breach_record_service.read_all_records(view=breach_record_view)

        breach_record_total = len(breach_record_pages)
        if breach_record_total > 0:
            summary = {
                'data_breach_record_count': breach_record_total,
                'data_breach_record_found': True
            }
            action_result.update_summary(summary)
            for breach_record_page in breach_record_pages:
                for breach_record in breach_record_page:
                    action_result.add_data(breach_record.payload)
            action_result.set_status(phantom.APP_SUCCESS, "Digital Shadows data breach records fetched")
        else:
            summary = {
                'data_breach_record_count': 0,
                'data_breach_record_found': False
            }
            action_result.update_summary(summary)
            action_result.set_status(phantom.APP_SUCCESS, "Data breach record not found in Digital Shadows")
        return action_result.get_status()

    def get_data_breach_record_reviews(self, param):
        action_result = ActionResult(dict(param))
        self._connector.add_action_result(action_result)
        breach_record_service = DataBreachRecordService(self._ds_api_key, self._ds_api_secret_key)

        breach_record_reviews = breach_record_service.find_data_breach_record_reviews(param['breach_record_id'])
        breach_record_reviews_total = len(breach_record_reviews)
        if breach_record_reviews_total > 0:
            summary = {
              'breach_record_reviews_count': breach_record_reviews_total,
              'breach_record_reviews_found': True
            }
            action_result.update_summary(summary)
            for breach_record_review in breach_record_reviews:
                action_result.add_data(breach_record_review)
            action_result.set_status(phantom.APP_SUCCESS, "Digital Shadows breach record reviews fetched for the Breach Record ID: {}".format(param['breach_record_id']))
        return action_result.get_status()

    def post_breach_record_review(self, param):
        action_result = ActionResult(dict(param))
        self._connector.add_action_result(action_result)
        breach_record_service = DataBreachRecordService(self._ds_api_key, self._ds_api_secret_key)
        post_data = {
          'note': param.get('review_note'),
          'status': param.get('review_status')
        }
        response = breach_record_service.post_data_breach_record_review(post_data, breach_record_id=param.get('breach_record_id'))

        if response['message'] == "SUCCESS":
            summary = {
              'breach_record_reviews_status_code': response['status'],
              'breach_record_reviews_message': response['message']
            }
            action_result.update_summary(summary)
            action_result.set_status(phantom.APP_SUCCESS, "Digital Shadows breach record review posted successfully")
        else:
            summary = {
              'breach_record_reviews_status_code': response['status'],
              'breach_record_reviews_message': response['message']
            }
            action_result.update_summary(summary)
            action_result.set_status(phantom.APP_SUCCESS, "Error in breach record review post request")
