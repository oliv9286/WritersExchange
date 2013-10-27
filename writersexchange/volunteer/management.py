
from volunteer.models import Program

def generate_field_list(volunteer):
    return [("Name", volunteer.name), ("Email", volunteer.email), 
            ("Phone #", volunteer.phone), ("Address", volunteer.address), 
            ("City", volunteer.city), ("Province", volunteer.province), 
            ("Reference #1", volunteer.reference1name), 
            ("Reference #1 Email", volunteer.reference1email),
            ("Reference #1 Phone", volunteer.reference1phone),
            ("Reference #2", volunteer.reference2name),
            ("Reference #2 Email", volunteer.reference2email),
            ("Reference #2 Phone", volunteer.reference2phone),
            ("Experience", volunteer.experience),
            ("Availability", volunteer.availability)]
def admin_is_logged_in():
  return True              #TODO do a proper check

def approve_application(volunteer):
  volunteer.isApproved = True      #TODO send necessary emails
  volunteer.save()

def reject_application(volunteer):
  volunteer.isApproved = False     #TODO send emails
  volunteer.delete()

def name_email_tuple(volunteer):
  return (volunteer.name, volunteer.email)

def program_for_name(name):
  programs = Program.objects.filter(name__exact=name)
  if len(programs) == 0:
      #no program with the given name exists, create it
      pForName = Program()
      pForName.name = name
      pForName.save()
  else:
      #use existing program
      pForName = programs[0]
  return pForName

