from checker.cc_frontend.web.models import Contest
from checker.cc_frontend.web.models import Problem
from checker.cc_frontend.web.models import Submission
from checker.cc_frontend.web.models import TestSet
from checker.cc_frontend.web.models import Testcase
import os
from storage_interface import Store


class Default(Store):

    """
    TODO: Implement the storage inferface for Django. See the API
    specification in storage_interface.py for details about how to
    implement the stubs below.
    """

    def __init__(self, config):
        self.config = config

    def get_submission(self):
        try :
            q_sub = Submission.objects.filter(result='QU')[0]
            src_fname = os.path.join(self.config.abs_path, str(q_sub.pk) +
                        '.' + q_sub.language)
            src_file = open(src_fname, 'w')
            src_file.write(q_sub.code)
            src_file.close()
            ret = { }
            ret['src_file'] = src_fname 
            ret['prob_id'] = str(q_sub.problem)
            ret['id'] = str(q_sub.pk)
            return ret

        except IndexError:
            print "No queued submission found"
            return None

    def set_compile_status(self, status, err_msg=None, submission_id=None):
        q_sub = Submission.objects.filter(pk=int(submission_id))
        q_sub.result = status
        q_sub.errors = err_msg
        q_sub.save()

    def get_all_testsets(self, problem_id=None):
        testsets = TestSet.objects.filter(problem=int(problem_id))
        for testset in testsets:
            ret_ts['prob_id'] = problem_id
            ret_ts['testset_id'] = str(testset.pk)
            ret_ts['timelimit'] = testset.timelimit
            ret_ts['memlimit'] = testset.memlimit
            ret_ts['score'] = testset.score 
            ret_ts['is_cust_scored'] = testset.is_cust_scored 
            ret_ts['cust_execute'] = testset.cust_executable 
            yield ret_ts

    def get_all_testcases(self, testset_id):
		testcases = Testcase.objects.filter(testset=testset_id)
		for testcase in testcases:
			ret_tc['infile'] = testcase.input
			ret_tc['reffile'] = testcase.output 
			ret_tc['testcase_id'] = testcase.pk
			yield ret_tc
	
    def set_testset_score(self, score, problem_id=None,
                             test_set_id=None, submission_id=None):
        pass

    def set_submission_run_status(self, status, submission_id=None):
        q_sub = Submission.objects.filter(pk=int(submission_id))
        q_sub.result = status
        q_sub.save()

    def set_submission_score(self, score, submission_id=None):
        q_sub = Submission.objects.filter(pk=int(submission_id))
        q_sub.score = score
        q_sub.save()
