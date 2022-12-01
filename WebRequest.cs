using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEngine.Networking;

public class WebRequest : MonoBehaviour
{
    private string url = "http://localhost:8585";
    public AgentList myAgentList = new AgentList();
    // public Agent a;

    // Text exchange;

    // public void GetExchangeRates()
    // {
    //     StartCoroutine(MakeRequest());
    // }

    IEnumerator MakeRequest()
    {
        UnityWebRequest request = UnityWebRequest.Get(url);
        yield return request.SendWebRequest();

        if (request.isNetworkError || request.isHttpError)
        {
            Debug.Log(request.error);
        }
        else
        {
            // Debug.Log("Received" + request.downloadHandler.text);
            JsonUtility.FromJsonOverwrite(request.downloadHandler.text, myAgentList);
            // for (int i = 0; i < myAgentList.Count; i++){
            //         print(myAgentList[i]);
            // }

            foreach (Agent a in myAgentList.agent_list) {
                Debug.Log("Agent_id: " + a.agent_id);
            }
            // var Rates = JsonConvert.DeserializeObject<Rates>(request.downloadHandler.text);

            // exchange = GameObject.Find("MainText").GetComponent<Text>();
            // exchange.text = Rates.ZAR.ToString();


        }
    }

    // Start is called before the first frame update
    void Start()
    {
        // StartCoroutine(MakeRequest());
        // Debug.Log("Starting script...");
    }

    // Update is called once per frame
    void Update()
    {
        StartCoroutine(MakeRequest());
        Debug.Log("Starting script...");
    }
}

public class Agent {
    public int agent_id;
    public int speed;
    public int lane;
}

public class AgentList {
    public List<Agent> agent_list;
}
