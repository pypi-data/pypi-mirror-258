from django.http import JsonResponse
from .response_view import statuscode

class ResultViewModel:
    def __init__(self):
        self.result = None
        self.errors = []
        self.success = True
    
    def add_result(self, model):
        self.result = model
        
    def add_errors(self, *msg:str):
        if len(msg) == 1 and isinstance(msg[0], list):
            self.errors.extend(msg[0])
        else:
            self.errors.extend(msg)
        self.success = False
    
def response(resultview : ResultViewModel = None, status_code: int = None) -> JsonResponse:
    if(status_code is None):
        status_code = statuscode.OK if resultview.success else statuscode.BAD_REQUEST
    return JsonResponse(resultview,status=status_code)
        
def success(model = None) -> JsonResponse:
    result_view_model = ResultViewModel()
    result_view_model.result = model
    result_view_model.success = True
    return JsonResponse(result_view_model.__dict__)
    
def bad_request(*msg:str) -> JsonResponse:
    result_view_model = ResultViewModel()
    if len(msg) == 1 and isinstance(msg[0], list):
        result_view_model.errors.extend(msg[0])
    else:
        result_view_model.errors.extend(msg)
    result_view_model.success = False
    return JsonResponse(result_view_model.__dict__, status=statuscode.BAD_REQUEST)