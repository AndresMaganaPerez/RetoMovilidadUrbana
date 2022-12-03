using System.Collections;
using System.Collections.Generic;
using UnityEditor.U2D;
using UnityEngine;

public class Car : MonoBehaviour
{
    public int id;
    public int lane;
    public int speed;
    public int newLane;
    public int turnSpeed = 3;


    void Start()
    {
        //if(lane == 0)
        //{
          //  transform.position = new Vector3(58.6f, 0.38f, -43.42f);
        //}
        //if (lane == 1)
        //{
          //  transform.position = new Vector3(58.6f, 0.38f, -45.48f);
        //}
        //if (lane == 2)
        //{
          //  transform.position = new Vector3(58.6f, 0.38f, -48.0f);
        //}
    }

    void Update()
    {
        Vector3 lane_0 = new Vector3(transform.position.x, transform.position.y, -43.42f);
        Vector3 lane_2 = new Vector3(transform.position.x, transform.position.y, -48.0f);

        if(newLane != lane)
        {
            lane = newLane;
            if (newLane == 0)
            {
                if(transform.position != lane_0)
                {
                    transform.Translate(Vector3.right* 70 * Time.deltaTime);
                }
            }
            if (newLane == 2)
            {
                if (transform.position != lane_2)
                {
                    transform.Translate(Vector3.left * 70 * Time.deltaTime);
                }
            }
            else
            {
                lane = newLane;
            }
        }
        
        transform.Translate(Vector3.forward * (speed * 5) * Time.deltaTime);
        

    }
  
}
