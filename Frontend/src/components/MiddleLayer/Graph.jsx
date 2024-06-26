import React, { useEffect, useState } from "react";
import useForm from "../context/useForm";
import Plot from "react-plotly.js";
import { useId } from "react";
import "../css/Graph.css";
import axios from "axios";
import Filter_box from "./Filter_box";
import { useRef } from "react";
import { useGSAP } from "@gsap/react";
import gsap from 'gsap'
function Graph() {
  const { user, setUser } = useForm();
  const array_of_filters = [
    [0, "Daily",useId()],[1, "week",useId()],
    [1, "month",useId()],
    [2, "month",useId()],
    [3, "month",useId()],
    [6, "month",useId()],
  ];
  const [filterobj, setFilterobj] = useState({});
  const [selectedId,setselectedId]=useState(array_of_filters[0][2])
  useEffect(() => {
    let { filter_range, val } = filterobj;
    let {Date_time,weekday,DeliverableQty_Numeric}=user;
    if (filter_range == undefined || val == undefined) return;
    axios
      .post("/api/fetch-data-filter", { filter_range, val,Date_time,weekday,DeliverableQty_Numeric })
      .then((response) => {
        setUser(response.data);
      })
      .catch((error) => console.log("error"));
  }, [filterobj]);
  console.log(user, "user");
const container=useRef()
 const boxesRef = useRef([]);
useGSAP(()=>{
   gsap.fromTo(
      container.current,
      { opacity: 0, y: 50 }, 
      { opacity: 1, y: 0, duration: 2, ease: 'power3.out' } 
    );

     

    // gsap.fromTo(
    //   boxesRef.current,
    //   { x: -100, opacity: 0 }, 
    //   {
    //     x: 0,
    //     opacity: 1,
    //     duration: 1,
    //     stagger: 0.3, 
    //     ease: 'power3.out',
    //   }
    // );
},[user])

  return (
    <>
      {user && (
        <div className="graphcontainer">
          
          <div className="upperpart" ref={container}>
            {
              <Plot
                data={[
                  {
                    x: user.x,
                    y: user.y,
                    type: "bar",
                    mode: "lines+markers",
                    name: "Deliverable Quantity",
                    marker: { color: "blue", size: 8 },
                    line: { smoothing: 1.3, color: "blue",width:1 },
                    opacity:0.8
                  },
                ]}
                layout={{
                  title: {
                    text: "Line Plot of Deliverable Quantity Over Time",
                    font: {
                      family: "Arial, sans-serif",
                      size: 24,
                      color: "purple",
                    },
                  },
                  xaxis: {
                    title: {
                      text: "Date",
                      font: {
                        family: "Arial, sans-serif",
                        size: 18,
                        color: "purple",
                      },
                    },
                    tickformat: "%d-%b-%Y",
                    showgrid: true,
                    zeroline: true,
                    gridcolor: "#e9e9e9",
                    color: "white",
                  },
                  yaxis: {
                    title: {
                      text: "Deliverable Quantity",
                      font: {
                        family: "Arial, sans-serif",
                        size: 18,
                        color: "purple",
                      },
                    },
                    showgrid: true,
                    zeroline: true,
                    gridcolor: "#e9e9e9",
                    color: "white",
                  },
                  template: "plotly",
                  width: 740,
                  height: 550,
                  margin: { t: 50, b: 50, l: 50, r: 50 },
                  paper_bgcolor: "#290439db",
                  plot_bgcolor: "#e5ecf6",
                  hovermode: "closest",
                }}
                config={{
                  responsive: true,
                  displayModeBar: true,

                  modeBarButtonsToRemove: [
                    "lasso2d",
                    "select2d",
                    "sendDataToCloud",
                    "zoomIn2d",
                    "zoomOut2d",
                    "autoScale2d",
                    "resetScale2d",
                    "toggleSpikelines",
                    "hoverClosestCartesian",
                    "hoverCompareCartesian",
                    "zoom2d",
                    "orbitRotation",
                    "v1hovermode",
                  ],
                }}
              />
            }
          </div>
          <div className="lowerpart">
{
    array_of_filters.map((element,index)=>{
      return (  <div className="parent" key={element[2]} style={selectedId==element[2]?{'backgroundColor':'black','transform':'scale(1.1)'}:{}} onClick={(e)=>{setselectedId(element[2])
        setFilterobj({filter_range:element[1],val:element[0]})
      }}
          ref={(el) => (boxesRef.current[index] = el)}
      >

        <Filter_box filter_range={element[1]} val={element[0]}  />
        </div>)
    })
}
          </div>

        </div>
      )}
    </>
  );
}

export default Graph;
