import React from "react";

function FilterButton(props) {
    return (
        // Filter buttons for tasks to show
            <button 
            type="button" 
            className="btn toggle-btn" 
            aria-pressed={props.isPressed} 
            onClick={() => props.setFilter(props.name)}>
            <span className="visually-hidden">Show </span>
            <span>{props.name}</span>
            <span className="visually-hidden"> plants</span>
            </button>
    );
}

export default FilterButton;
