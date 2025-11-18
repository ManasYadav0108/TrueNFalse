from azure.eventhub import EventHubConsumerClient
import pandas as pd
def get_eventhub_df(conn_dict):
    conn_str = conn_dict["connection_string"]
    eventhub_name = conn_dict["eventhub_name"]
    events_list = []
    def on_event(partition_context, event):
        events_list.append(event.body_as_str())
    client = EventHubConsumerClient.from_connection_string(
        conn_str, consumer_group="$Default", eventhub_name=eventhub_name
    )
    client.receive(on_event=on_event, max_wait_time=5)
    client.close()
    return pd.DataFrame({"events": events_list})