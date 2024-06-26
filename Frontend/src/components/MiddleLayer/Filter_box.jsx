import React from "react";

function filter_box({ filter_range, val }) {
  return (
    <>
      <div className="box">
        {val == 0 ? "" : val}
        {filter_range[0].toUpperCase()}
      </div>
    </>
  );
}

export default filter_box;
