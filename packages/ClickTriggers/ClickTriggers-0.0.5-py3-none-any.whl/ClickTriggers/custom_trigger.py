from __future__ import annotations
import asyncio
from typing import Any
from airflow.triggers.base import BaseTrigger, TriggerEvent
from airflow.models import XCom

class CustomTrigger(BaseTrigger):
    """
    Trigger based on a datetime.

    A trigger that fires exactly once, at the given datetime, give or take
    a few seconds.

    The provided datetime MUST be in UTC.
    """

    def __init__(self, dag_id, dag_run_id, task_id, xcom_key, 
                 loop_status_key, context, execution_date):
        super().__init__()
        # self.idx = 0
        self.dag_id = dag_id
        self.dag_run_id = dag_run_id
        self.task_id = task_id
        self.xcom_key = xcom_key
        self.execution_date = execution_date
        self.context = context
        self.loop_status_key = loop_status_key
        #self.moment = moment

    def serialize(self) -> tuple[str, dict[str, Any]]:
        return ("ClickTriggers.custom_trigger.CustomTrigger", {"dag_id": self.dag_id, 
                                                           "dag_run_id": self.dag_run_id, 
                                                           "task_id": self.task_id, 
                                                           "xcom_key": self.xcom_key, 
                                                           'context': self.context,
                                                           'loop_status_key': self.loop_status_key,
                                                           'execution_date': self.execution_date})

    def get_status(self):
        condition = XCom.get_one(key=self.xcom_key, task_id=self.task_id, dag_id=self.dag_id, run_id=self.dag_run_id)

        reason = XCom.get_one(key=self.loop_status_key, task_id=self.task_id, 
                              dag_id = self.dag_id, run_id=self.dag_run_id) or {}
        self.log.info(f"condition {condition}")
        self.log.info(f" reason {reason}")
        loop_state = reason.get("State", "HALT")
        self.log.info(f"{loop_state}")

        return condition  and not ( 
            loop_state.upper() == "FAILED" or
            loop_state.upper() == "HALT"
        )

    async def run(self):

        self.log.info("trigger starting")
        status = self.get_status()
        self.log.info("trigger starting",status)

        while status:
            self.log.info(f"sleeping 1 second... {status}")
            await asyncio.sleep(1)
            status = self.get_status()

        yield TriggerEvent(self.context)
