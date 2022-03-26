from flask import Flask, jsonify, request, make_response,jsonify, json
class Return:
    @staticmethod
    def returnResponse(object,code):
       
        response = make_response(   
                jsonify(
                    {"Obj": json.loads(json.dumps(object))}
                ),
                code
            )
        response.headers["Content-Type"] = "application/json"
        
        return response
