# prefect_supporter

prefect_supporter provide services to supporter to manage Prefect

## Usage

1. Delete `flow run` history in Database. It also deletes `task run`
   - create your deployment
      - example  
      ```python
        
        from datetime import datetime, timedelta
    
        from prefect.settings import PREFECT_API_URL
        from prefect.deployments import Deployment
        from prefect.server.schemas.schedules import CronSchedule
        from prefect.server.schemas.states import StateType
        from prefect_supporter.flow import clear_db_history
        from prefect_supporter.flow.clear_db_history import clear_db_history_flow
        from prefect_supporter.model.clearing_db import FlowRunClearing
        
        Deployment.build_from_flow(
            flow=clear_db_history_flow,
            name="clear_db_history_deployment",
            schedule=CronSchedule(cron="0 * * * *", ),
            work_queue_name="default",
            tags=["prefect-management"],
            entrypoint=f"{clear_db_history.__file__}:clear_db_history_flow",
            parameters={
                "frc": FlowRunClearing(
                    api_url=PREFECT_API_URL.value(),
                    state_list=[StateType.COMPLETED],
                    before_dt=(datetime.now() - timedelta(days=7)),
                    after_dt=datetime(year=1970, month=1, day=1, hour=0, minute=0)
                )
            },
            apply=True
        )
      ```
     
  - Parameter   
      - `FlowRunClearing` model
         - api_url : your prefect api address, ex) http://localhost:4200/api
         - state_list: state list to delete ex) "COMPLETED", "FAILED"
         - before_dt : time range to delete data to be started
         - after_dt : time range to delete data  to be ended