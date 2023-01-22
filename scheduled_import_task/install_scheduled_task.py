import datetime
import win32com.client

TASK_TRIGGER_DAILY = 2
TASK_ACTION_EXEC = 0
TASK_CREATE_OR_UPDATE = 6
TASK_LOGON_NONE = 0

if __name__ == "__main__":

    scheduler = win32com.client.Dispatch('Schedule.Service')
    scheduler.Connect()
    root_folder = scheduler.GetFolder('\\')
    task_def = scheduler.NewTask(0)
    
    # How the task will be triggered. This  task will repeat every MINS mins.
    # This means that the importer will attempt to import an item in to the media library every MINS mins  
    
    trigger = task_def.Triggers.Create(TASK_TRIGGER_DAILY)
    trigger.StartBoundary = datetime.datetime.now().isoformat() # task will start at this time every day. 
    
    MINS = 15 # minutes 
    
    trigger.Repetition.Duration = '' # If no value is specified for the duration, then the pattern is repeated indefinitely.
    trigger.Repetition.Interval = 'PT' + str(MINS) + 'M' # every MINS the task will run. "PT20M" is 20 minutes
    trigger.Repetition.StopAtDurationEnd = False #  a Boolean  indicates if a running instance of  task is stopped at the end of the repetition pattern duration.
    
    # What the task will execute once it is triggered
    ACTION_ID = 'Import' # used for logging to show what action occurred. 
    EXE_PATH = 'python' # what will be executed
    ARGS = '' # its args 
    
    action = task_def.Actions.Create(TASK_ACTION_EXEC)
    action.ID = ACTION_ID
    action.Path = EXE_PATH
    action.Arguments = ARGS

    # Task  parameters
    TASK_DESCRIPTION = 'Fatboy Home Network Media Library Importer. '
    
    task_def.RegistrationInfo.Description = TASK_DESCRIPTION
    task_def.Settings.Enabled = True
    task_def.Settings.StopIfGoingOnBatteries = False
    
    # Register task, If task already exists, it will be updated
    TASK_NAME = 'Media Library Import'
    USER_NAME = ''
    USER_PASSWORD = ''
    
    root_folder.RegisterTaskDefinition(TASK_NAME, task_def, TASK_CREATE_OR_UPDATE, USER_NAME, USER_PASSWORD, TASK_LOGON_NONE)
    
