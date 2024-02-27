from enum import Enum

VALID_JOB_STATUS:list = ["SUCCESS", "FINISHED"]

class JobType(Enum):
    API = "API"
    UX = "UX"
    UNKNOWN = "UNKNOWN"

class ComplianceEvaluator:

    job_execution_result:dict
    tolerance:dict

    def __init__(self, job_execution_result:dict, tolerance:dict) -> None:
        self.job_execution_result = job_execution_result
        self.tolerance = tolerance

    def __validate_job__(self) -> list:
        result_list:list = []

        if not "status" in self.job_execution_result:
            result_list.append('job without status')
        elif not self.job_execution_result["status"] in VALID_JOB_STATUS:
            result_list.append(f"job status is not in {VALID_JOB_STATUS}")

        return result_list            

    def __evaluate_job_api__(self) -> list:
        current_value:float = 0.0
        minimum:float = 0.0
        error_messagges:list = []

        validation_list:list = self.__validate_job__()

        if len(validation_list) == 0:
            current_value = float(self.job_execution_result['complianceLatency'])
            minimum = self.tolerance['latency'] * 100
            if (current_value < minimum):
                error_messagges.append('Latency {} below tolerance {}'.format(current_value, minimum))

            current_value = float(self.job_execution_result['complianceThroughput'])
            minimum = self.tolerance['throughput'] * 100
            if (current_value < minimum):
                error_messagges.append('Throughput {} below tolerance {}'.format(current_value, minimum))

            current_value = float(self.job_execution_result['complianceErrors'])
            minimum = self.tolerance['errors'] * 100
            if (current_value < minimum):
                error_messagges.append('Errors {} below tolerance {}'.format(current_value, minimum))

            current_value = float(self.job_execution_result['complianceDeviation'])
            minimum = self.tolerance['deviation'] * 100
            if (current_value < minimum):
                error_messagges.append('Deviation {} below tolerance {}'.format(current_value, minimum))
        else:
            error_messagges = validation_list

        return error_messagges if len(error_messagges) > 0 else None

    def __evaluate_job_ux__(self) ->list:
        raise Exception("Not implemented")

    def __is_ux_job__(self) -> bool:
        return "uxResults" in self.job_execution_result
    
    def __is_api_job__(self) -> bool:
        return "kpiLatency" in self.job_execution_result

    def __get_job_type__(self) -> JobType:
        if self.__is_ux_job__():
            return JobType.UX
        elif self.__is_api_job__():
            return JobType.API
        return JobType.UNKNOWN

    def evaluate(self) -> list:
        job_type:JobType = self.__get_job_type__()
        if job_type == JobType.API:
            return self.__evaluate_job_api__()
        elif job_type == JobType.UX:
            return self.__evaluate_job_ux__()
        raise Exception("Invalid Job Type")