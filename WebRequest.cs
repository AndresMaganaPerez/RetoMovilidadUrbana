using Newtonsoft.Json.Linq;
using System;
using System.Collections;
using System.Collections.Generic;
using System.Net.NetworkInformation;
using System.Reflection;
using Unity.VisualScripting;
using UnityEditor;
using UnityEngine;
using UnityEngine.Networking;

public class WebRequest : MonoBehaviour
{
    private string url = "http://localhost:8585";
    public List<Agent> agentes = new List<Agent>();
    public bool flag;
    public int auxIndex;
    public int contador = 0;
    public GameObject carPrefab;
    public List<GameObject> carros = new List<GameObject>();
    public Vector3 startPoint;
    
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
            //Debug.Log("Received" + request.downloadHandler.text);
            //Agent agente = new Agent();


            string txt = request.downloadHandler.text.Replace('\'', '\"');
            txt = txt.TrimStart('"', '{', 'a', 'g', 'e', 'n', 't', 's', ':', '[');
            txt = "{\"" + txt;
            txt = txt.TrimEnd(']', '}');
            txt = txt + '}';
            //Debug.Log("BLAH: " + txt);
            string[] strs = txt.Split(new string[] { "}, {" }, StringSplitOptions.None);
            //Debug.Log("strs.Length:" + strs.Length);
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

                
                Agent a = JsonUtility.FromJson<Agent>(strs[i]);

                agentes.Add(a);
                a.spawned= true;
            }
            spawnCars(agentes, 0);
            
        }

    }




    IEnumerator MakeRequest2()
    {
        UnityWebRequest request = UnityWebRequest.Get(url);
        yield return request.SendWebRequest();

        if (request.isNetworkError || request.isHttpError)
        {
            Debug.Log(request.error);
        }
        else
        {
            
            //Debug.Log("Received" + request.downloadHandler.text);
            //Agent agente = new Agent();


            string txt = request.downloadHandler.text.Replace('\'', '\"');
            txt = txt.TrimStart('"', '{', 'a', 'g', 'e', 'n', 't', 's', ':', '[');
            txt = "{\"" + txt;
            txt = txt.TrimEnd(']', '}');
            txt = txt + '}';
            //Debug.Log("BLAH: " + txt);
            string[] strs = txt.Split(new string[] { "}, {" }, StringSplitOptions.None);
            //Debug.Log("strs.Length:" + strs.Length);
            for (int i = 0; i < strs.Length; i++)
            {
                flag = false;
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
                char lastSymbol = strs[i][strs[i].Length - 1];
                char lastlastSymbol = strs[i][strs[i].Length - 2];
                if (lastlastSymbol == '}' && lastSymbol == '}')
                {
                    strs[i] = strs[i].Remove(strs[i].Length - 1);
                }

                //Debug.Log(strs.Length);
                //Debug.Log(strs[i]);
                Agent a = JsonUtility.FromJson<Agent>(strs[i]);

                //Debug.Log("ID DEL AGENTE: " + a.id);
                //Debug.Log("LANE: " + a.lane);
                //Debug.Log("VELOCIDAD: " + a.speed);
                //Debug.Log("NUM AGENTS: " + a.num_agents);
                
                for(int j = 0; j < agentes.Count; j++)
                {
                    //Debug.Log("Agentes id: " + agentes[j].id);
                    //Debug.Log("J ITERADOR:" + j);
                    //Debug.Log("A id: " + a.id);
                    //Debug.Log(a.id == agentes[j].id);
                    if(a.id == agentes[j].id)
                    {
                        a.flag = true;
                        auxIndex = j;
                        //Debug.Log("FLAG: " + flag);
                    }
                    else if (a.id > agentes.Count)
                    {
                        a.flag = false;
                        //Debug.Log("FLAG" + flag);
                    }

                }
                //Debug.Log(a.flag);
                if(a.flag == true)
                {
                    //Debug.Log("BANDERA VERDADERA");
                    agentes[auxIndex].speed = a.speed;
                    agentes[auxIndex].lane = a.lane;
                    carros[auxIndex].GetComponent<Car>().speed = a.speed;
                    carros[auxIndex].GetComponent<Car>().newLane = a.lane;

                } else if(a.flag == false)
                {
                    //Debug.Log("BANDERA FALSA");
                    agentes.Add(a);
                    Debug.Log("COUNT: " + agentes.Count);
                }
                for (int k = 0; k < agentes.Count; k++)
                {
                    if (agentes[k].spawned == false)
                    {
                        spawnCars(agentes, k);
                        agentes[k].spawned = true;
                    }
                }

            }
            
        }
    }







    // Start is called before the first frame update
    void Start()
    {
        contador += 1;
        StartCoroutine(MakeRequest());
        StartCoroutine(MakeRequest());
    }

    // Update is called once per frame
    void Update()
    {
        contador += 1;
        if(contador == 50)
        {
            Debug.Log("UPDATE");
            StartCoroutine(MakeRequest2());
            contador = 0;
        }
        //Debug.Log("Starting script...");
    }

    void spawnCars(List<Agent> listaAgentes, int index)
    {
        if (listaAgentes[index].lane == 0)
        {
            startPoint = new Vector3(58.90f, 0, -43.35f);
        }
        if (listaAgentes[index].lane == 1)
        {
            startPoint = new Vector3(58.90f, 0, -45.48f);
        }
        if (listaAgentes[index].lane == 2)
        {
            startPoint = new Vector3(58.90f, 0, -48.0f);
        }
        GameObject carrito = Instantiate(carPrefab, startPoint, transform.rotation);
        carrito.GetComponent<Car>().id = listaAgentes[index].id;
        carrito.GetComponent<Car>().lane = listaAgentes[index].lane;
        carrito.GetComponent<Car>().speed = listaAgentes[index].speed;
        carrito.GetComponent<Car>().newLane = listaAgentes[index].lane;
        carros.Add(carrito);
        Debug.Log("CARROS: " + carros.Count);
    }
    
}


[System.Serializable]
public class Agent
{
    public int id;
    public int lane;
    public int speed;
    public int num_agents;
    public bool spawned = false;
    public bool flag = false;
}


