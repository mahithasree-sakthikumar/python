# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from airtable import Airtable
from ask_sdk_model import Response

# Establish connection with the airtable table_name

base_id = 'appaMOte1pv9ing8Q'
teacher_table = 'teacher'
student_table = 'student'
api_key = 'keylcn5bQnjdFOAls'

table1 = Airtable(base_id, teacher_table, api_key)
table2 = Airtable(base_id, student_table, api_key)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Launch Request

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome, you can say sign up or login . Which would you like to try?"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# Registration Handler

class RegistrationHandler(AbstractRequestHandler):
    """Handler for Registration Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("Registration")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        profession = ask_utils.request_util.get_slot(handler_input, "profession").value
        first_name = ask_utils.request_util.get_slot(handler_input, "First_Name").value
        last_name = ask_utils.request_util.get_slot(handler_input, "Last_Name").value
        gender = ask_utils.request_util.get_slot(handler_input, "Gender").value
        number = ask_utils.request_util.get_slot(handler_input, "Mobile_No").value
        Point = 0
        password = str(number)
        password = password[6:]
        if len(number)==10:
            if profession == 'teacher':
                record = {'First_Name':first_name,'Last_Name':last_name,'Gender':gender,'Mobile_No':number,'Point':Point}
                table1.insert(record)
                speak_output = " Teacher details insert successfully, your login ID is REW{} and password is {} ,say ok".format(number,password)
            elif profession == 'student':
                record = {'First_Name':first_name,'Last_Name':last_name,'Gender':gender,'Mobile_No':number,'Point':Point}
                table2.insert(record) 
                speak_output = "Student detail insert successfully, your login ID is REW{} and password is {} ,say ok".format(number,password)
            else :
                speak_output = "You insert wrong profession."
        else:
            speak_output = "Incorrect mobile number, Registration fail"
        
        
        reprompt="Now, you can login"
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt)
                .response
        )

# Login Handler

class LoginHandler(AbstractRequestHandler):
    """Handler for Login of user ."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("Login")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        profession = ask_utils.request_util.get_slot(handler_input, "profession").value
        loginID = ask_utils.request_util.get_slot(handler_input, "LoginID").value
        password = ask_utils.request_util.get_slot(handler_input, "password").value
        loginID = str('REW')+loginID
        if profession == 'student':
            student_ID = table2.match('Login_ID', loginID)
            student_pass = student_ID['fields']['Password']
            student_name = student_ID['fields']['First_Name']
            
            if student_pass==password:
                speak_output = "Login Sucessful, Welcome {}".format(student_name)
                handler_input.attributes_manager.session_attributes["Login_ID"] = loginID
                handler_input.attributes_manager.session_attributes["profession"] = profession
            else:
                speak_output = "Wrong Information"
        elif profession == 'teacher':
            teacher_ID = table1.match('Login_ID', loginID)
            teacher_pass = teacher_ID['fields']['Password']
            teacher_name = teacher_ID['fields']['First_Name']
            if teacher_pass==password:
                speak_output = "Login Sucessful, Welcome {}".format(teacher_name)
                handler_input.attributes_manager.session_attributes["Login_ID"] = loginID
                handler_input.attributes_manager.session_attributes["profession"] = profession
            else:
                speak_output = "Wrong Information"
        else:
            speak_output = "invalid"
            reprompt = "now , you can view your profile "

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt)
                .response
        )
# Profile Handler
class ProfileHandler(AbstractRequestHandler):
    """Handler for Profile"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("Profile")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        profession = handler_input.attributes_manager.session_attributes["profession"]
        if profession=='student':
            try:
                loginID = handler_input.attributes_manager.session_attributes["Login_ID"]
                ID = table2.match('Login_ID', loginID)
            except:
                loginID = False
        elif profession=='teacher':
            try:
                loginID = handler_input.attributes_manager.session_attributes["Login_ID"]
                ID = table1.match('Login_ID', loginID)
            except:
                loginID = False
        first_name = ID['fields']['First_Name']
        last_name = ID['fields']['Last_Name']
        gender = ID['fields']['Gender']
        number = ID['fields']['Mobile_No']
        speak_output = "Your name is {} {}, gender is {}, Mobile number is {}".format(first_name,last_name,gender,number)

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
# student Roll Number Handler
class MyRollNoHandler(AbstractRequestHandler):
    """Handler for Roll No."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("MyRollNo")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        profession =handler_input.attributes_manager.session_attributes["profession"]
        if profession=='student':
            try:
                loginID =handler_input.attributes_manager.session_attributes["Login_ID"]
                student_ID = table2.match('Login_ID', loginID)
                student_rollno = student_ID['fields']['Roll_Number']
            except:
                loginID = False
            
            speak_output = "Your roll number is {}".format(student_rollno)

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
# Student and Teacher Point Handler
class ViewMyPointHandler(AbstractRequestHandler):
    """Handler for View My Point"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ViewMyPoint")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        profession = handler_input.attributes_manager.session_attributes["profession"]
        if profession=='student':
            try:
                loginID = handler_input.attributes_manager.session_attributes["Login_ID"]
                student_ID = table2.match('Login_ID', loginID)
                student_Point = student_ID['fields']['Point']
            except:
                loginID = False
            
            speak_output = "Your point is {}".format(student_Point)
        elif profession=='teacher':
            try:
                loginID = handler_input.attributes_manager.session_attributes["Login_ID"]
                teacher_ID = table1.match('Login_ID', loginID)
                teacher_Point = teacher_ID['fields']['Point']
            except:
                loginID = False
            
            speak_output = "Your point is {}".format(teacher_Point)

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
class ViewOtherPointHandler(AbstractRequestHandler):
    """Handler for View Other Point"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ViewOtherPoint")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        profession = ask_utils.request_util.get_slot(handler_input, "profession").value
        num = ask_utils.request_util.get_slot(handler_input, "MobileNo").value
        num = str("REW")+num
        if profession=='student':
            student_ID = table2.match('Login_ID', num)
            student_Point = student_ID['fields']['Point']
            speak_output = "Point is {}".format(student_Point)
        elif profession=='teacher':
            teacher_ID = table1.match('Login_ID', num)
            teacher_Point = teacher_ID['fields']['Point']
            speak_output = "Point is {}".format(teacher_Point)
        #speak_output = "{} {} point is {}".format(first_name,last_name,point)

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
# Teacher Point Handler
class TeacherPointIncrementHandler(AbstractRequestHandler):
    """Handler for Teacher Point Increment"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("TeacherPointIncrement")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        profession = handler_input.attributes_manager.session_attributes["profession"]
        if profession=='teacher':
            loginID = handler_input.attributes_manager.session_attributes["Login_ID"]
                
            teacher_ID = table1.match('Login_ID', loginID)
            Point = teacher_ID['fields']['Point']
            Point=Point+5
            updated_detail = {'Point': Point}
            table1.update_by_field('Login_ID',loginID, updated_detail)
            speak_output = "Teacher point incremented and point is {}".format(Point)
        

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


# Student Point Handler
class StudentPointIncrementHandler(AbstractRequestHandler):
    """Handler for Student Point Increment"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("StudentPointIncrement")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        profession = handler_input.attributes_manager.session_attributes["profession"]
        RollNo = handler_input.request_envelope.request.intent.slots["RollNo"].value
        if profession=='teacher':
            
            
            student_rollno = table2.match('Roll_Number', RollNo)
            Point = student_rollno['fields']['Point']
            Point=Point+5
            updated_detail = {'Point': Point}
            table2.update_by_field('Roll_Number',RollNo, updated_detail)
        
        speak_output = "Student point awarded and point is {}".format(Point)
        

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class LogoutHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("Logout")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Logout Sucessful"
        handler_input.attributes_manager.session_attributes["Login_ID"] = None
        handler_input.attributes_manager.session_attributes["profession"] = None

        return (
            handler_input.response_builder
                .speak(speak_output)
                .set_should_end_session(True)
                .ask(speak_output)
                .response
        )

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(RegistrationHandler())
sb.add_request_handler(LoginHandler())
sb.add_request_handler(ProfileHandler())
sb.add_request_handler(MyRollNoHandler())
sb.add_request_handler(ViewMyPointHandler())
sb.add_request_handler(ViewOtherPointHandler())
sb.add_request_handler(TeacherPointIncrementHandler())
sb.add_request_handler(StudentPointIncrementHandler())
sb.add_request_handler(LogoutHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()