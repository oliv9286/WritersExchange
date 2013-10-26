
def admin_is_logged_in():
  return True              #TODO do a proper check

def approve_application(volunteer):
  volunteer.isApproved = True      #TODO send necessary emails
  volunteer.save()

def reject_application(volunteer):
  volunteer.isApproved = False     #TODO send emails
  volunteer.delete()

