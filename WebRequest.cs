using Newtonsoft.Json.Linq;
using System;
using System.Collections;
using System.Collections.Generic;
using System.Net.NetworkInformation;
using Unity.VisualScripting;
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
            txt = txt.TrimStart('"', '{', 'a', 'g', 'e', 'n', 't', 's', ':', '[');
            txt = "{\"" + txt;
            txt = txt.TrimEnd(']', '}');
            txt = txt + '}';
            Debug.Log("BLAH: " + txt);
            string[] strs = txt.Split(new string[] { "}, {" }, StringSplitOptions.None);
            Debug.Log("strs.Length:" + strs.Length);
            for (int i = 0; i < strs.Length; i++)
            {
                strs[i] = strs[i].Trim();
                if (i == 0)
                {
                    strs[i] = strs[i] + '}';
                }
                else if (i == strs.Length - 1)
                {
                    strs[i] = '{' + strs[i];
                }
                else
                {
                    strs[i] = '{' + strs[i] + '}';
                }
                char lastSymbol = strs[i][strs[i].Length-1];
                char lastlastSymbol = strs[i][strs[i].Length - 2];
                if (lastlastSymbol == '}' && lastSymbol == '}')
                {
                    strs[i] = strs[i].Remove(strs[i].Length-1);
                }
                Debug.Log(strs[i]);
                Agent a = JsonUtility.FromJson<Agent>(strs[i]);
                Debug.Log("ID DEL AGENTE: " + a.id);
                Debug.Log("LANE: " + a.lane);
                Debug.Log("VELOCIDAD: " + a.speed);
                
                //JObject json = JObject.Parse(txt);
                //Debug.Log("EL JSON DEL AGENTE ES: " + json);
                //string id = json.First.ToString();
                //string lane = json.First.Previous.ToString();
                //string speed = json.Last.ToString();
                //id = id.Trim('"', 'i', 'd', '"', ':');
                //lane = lane.Trim('"', 'l', 'a', 'n', 'e', '"', ':');
                //speed = speed.Trim('"', 's', 'p', 'e', 'e', 'd', '"', ':');
                //Debug.Log("EL ID DEL AGENTES ES: " + id);
                //Debug.Log("EL LANE DEL AGENTES ES: " + lane);
                //Debug.Log("EL SPEED DEL AGENTES ES: " + speed);

                //Agent a = JsonUtility.FromJson<Agent>(json);
                //Debug.Log("IDENTIDAD: " + a.id);
                //char[] charsToTrim = {'{', '"','}',':','i','d','l','a','n','e'}; 
                //strs[i] = strs[i].Trim(charsToTrim);
                //Debug.Log(strs[i]);

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


