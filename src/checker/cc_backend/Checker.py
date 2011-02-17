#!/usr/bin
import sys
import os
import string
import time
import threading

from store.default_store import Default
from evaluator.eval import Evaluate
from compiler.compile import Compiler
from score.score import Score
from Config import Config


def wait_for_submission(store):
    """
    Returns a submission to be evaluated. Blocks execution until one
    is available.
    """
    is_waiting = False
    while True:
        submission = store.get_submission()
        if submission is not None:
            yield submission
        else:
            if not is_waiting:
                is_waiting = True
                print "Waiting for a submission."
            time.sleep(2)


def compile_submission(store, submission):
    """
    Attempts to compile the submission. Updates the status in the
    store. Return True or False.
    """
    compiler_res = compiler.compile_source(submission["src_file"])
    if compiler_res["retcode"] == 0:
        store.set_compile_status("COMPILED", err_msg=None,
                                 sub_id=submission["id"])
        return compiler_res
    else:
        store.set_compile_status("COMPILATION ERROR",
                                 err_msg=status_info.err_msg,
                                 sub_id=submission["id"])
        return None


def main():

    config = Config("conf/codechecker.conf")
    store = Default(config)
    evaluator = Evaluate(config)
    compiler = Compiler(config)
    score = Score()

    # Each iteration of the loop below evalutes a submission.
    for submission in wait_for_submission(store):

        # compile the submission
        compiler_res = compile_submission(store, submission)
        if compiler_res == None:
            continue

        # Evaluate the queued submission. Somewhere in the following
        # loop it is also possible that the program fails - need to
        # set the status to runtime error status.
        test_group_scores = []
        for testset in store.get_all_testsets(submission["prob_id"]):
            testset_info = {}
            testset_info["memlimit"] = testset["memlimit"]
            testset_info["timelimit"] = testset["timelimit"]
            testset_info["cust_execute"] = testset["cust_execute"]
            testset_info["is_cust_scored"] = testset["is_cust_scored"]
            testset_info["infile"] = []
            testset_info["reffile"] = []
            for testcase in store.get_all_testcases(testset["testset_id"]):
                testset_info["infile"].append(testcase["infile"])
                testset_info["reffile"].append(testcase["reffile"])

            result_set = evaluator.eval_submission(submission,
                                                   testset_info,
                                                   compiler_res["run_cmd"])
            #TODO: implement the below functions properly.
            test_grp_score = score.score_group(prob_id,
                                               result_set)
            store.set_test_group_score(test_grp_score,
                                       problem_id=prob_id,
                                       test_group_id=test_grp["id"],
                                       submission_id=submission["id"])
            test_group_scores.append(test_grp_score)

        # compute and set the overall score.
        final_score = score.overall(test_group_scores,
                                    problem_id=prob_id)
        store.set_submission_score(final_score,
                                   submission_id=submission["id"])
        store.set_submission_run_status("PASS",
                                        submission_id=submission["id"])


if __name__ == '__main__':
    main()
