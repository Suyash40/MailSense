class ActionAgent:

    def process(self, category, extracted_info):
        actions = {
            "task_created": None,
            "alert": False
        }

        # Create task if action item exists
        if extracted_info.get("action_item"):
            actions["task_created"] = extracted_info["action_item"]

        # Trigger alert if urgent
        if category == "urgent":
            actions["alert"] = True

        return actions
