from datetime import datetime

import hubspot
from pprint import pprint
from hubspot.crm.tickets import SimplePublicObjectInputForCreate, ApiException
from hubspot.crm.objects.notes import SimplePublicObjectInputForCreate, ApiException

client = hubspot.Client.create(access_token="")


def create_ticket(list_of_messages):
    properties = {
        "hs_pipeline": "0",
        "hs_pipeline_stage": "1",
        "hs_ticket_priority": "LOW",
        "subject": "AI Assistant Conversation",
    }

    # associations = [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 16}]

    input = SimplePublicObjectInputForCreate(associations=[], properties=properties)

    try:
        api_response = client.crm.tickets.basic_api.create(
            simple_public_object_input_for_create=input)
        pprint(api_response)
        create_task(api_response.id)
        create_note(api_response.id, list_of_messages, None)
    except ApiException as e:
        print("Exception when calling basic_api->create: %s\n" % e)


def create_task(ticket_id):
    current_time = datetime.utcnow()
    properties = {
        "hs_task_body": "Review the attached note and review conversation for accuracy",
        "hs_timestamp": current_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
        "hs_task_status": "WAITING",
        "hs_task_subject": "AI Conversation Review",
        "hs_task_priority": "MEDIUM",
    }

    associations = [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 230}]

    simple_public_object_input_for_create = SimplePublicObjectInputForCreate(associations=[
        {"to": {"id": ticket_id}, "types": associations}], properties=properties)
    try:
        api_response = client.crm.objects.tasks.basic_api.create(
            simple_public_object_input_for_create=simple_public_object_input_for_create)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling basic_api->create: %s\n" % e)


def create_note(ticket_id, list_of_messages, contact_id=None):
    current_time = datetime.utcnow()
    properties = {
        "hs_note_body": "AI Conversation:  <br/> ---------------------------------------- ",
        "hs_timestamp": current_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
    }

    # add list_of_messages to note body
    for message in list_of_messages:
        properties["hs_note_body"] += "<br/>" + message

    note = SimplePublicObjectInputForCreate(associations=[
        {"to": {"id": ticket_id}, "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 228}]}],
        properties=properties)

    if contact_id != None:
        note.associations.append(
            {"to": {"id": contact_id}, "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 202}]})
    else:
        note.properties["hs_note_body"] = "WARNING - NO KNOWN CONTACT FOUND <br/><br/>" + note.properties[
            "hs_note_body"]
    try:
        api_response = client.crm.objects.notes.basic_api.create(
            simple_public_object_input_for_create=note)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling basic_api->create: %s\n" % e)
