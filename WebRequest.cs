using System;
using System.Collections;
using System.Collections.Generic;
using System.Net.NetworkInformation;
using UnityEditor;
using UnityEngine;
using UnityEngine.Networking;

public class WebRequest : MonoBehaviour
{
    private string url = "http://localhost:8585";
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
            Debug.Log("Received" + request.downloadHandler.text);
            Agent agente = new Agent();


            string txt = request.downloadHandler.text.Replace('\'', '\"');
            txt = txt.TrimStart('"', '{', 'd', 'a', 't', 'a', ':', '[');
            txt = "{\"" + txt;
            txt = txt.TrimEnd(']', '}');
            txt = txt + '}';
            string[] strs = txt.Split(new string[] { "}, {" }, StringSplitOptions.None);
            Debug.Log("strs.Length:" + strs.Length);
            for (int i = 0; i < strs.Length; i++)
            {
                strs[i] = strs[i].Trim();
                if (i == 0)
                {
                    strs[i] = strs[i] + ']';
                }
                else if (i == strs.Length - 1)
                {
                    strs[i] = '{' + strs[i];
                }
                else
                {
                    strs[i] = '{' + strs[i] + '}';
                }
                Debug.Log(strs[i]);
                //RootObject ag = JsonUtility.FromJson<RootObject>("{\"users\":" + strs[i] + "}");
                //Debug.Log(ag);
                //Agent a = JsonUtility.FromJson<Agent>(strs[i]);
                //Debug.Log("VELOCIDAD: " + a.speed);
            }
        }
    }

    // Start is called before the first frame update
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {
        StartCoroutine(MakeRequest());
        Debug.Log("Starting script...");
    }
}

[System.Serializable]
public class Agent
{
    public int id;
    public int lane;
    public int speed;
}

[System.Serializable]
public class RootObject
{
    public Agent[] agentes;
}