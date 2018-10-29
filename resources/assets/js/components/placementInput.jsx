import React, { Component } from 'react';
import webUrl from '../abstract/variables';
import axios from 'axios';

class PlacementInput extends Component {
    constructor(props){
        super(props);

        this.state = {
            name: "",
            activeInput:false,
            lastTyped: Date.now(),
            suggestions:[],
            limit:this.props.limit == undefined ? 1 : this.props.limit
        }

        this.handleNameChange = this.handleNameChange.bind(this);
        this.toggleInput = this.toggleInput.bind(this);
        this.selectPlacement = this.selectPlacement.bind(this);
    }

    toggleInput(){
        var state = this.state;
        state.activeInput = state.activeInput == true ? false : true;
        state.suggestions =[];
        state.name = "";
        this.setState(state);
    }

    handleNameChange(e){
        var c = this;
        var state = c.state;
        state.name = e.target.value;
        state.lastTyped = Date.now();
        c.setState(state);

        setTimeout(()=>{
            var last = c.state.lastTyped;

            if ((Date.now() - last)>=1000) {
                c.getPlacementSuggestions();
            }
        },1000);
    }

    selectPlacement(item){
        var state = this.props.parent.state;

        var index = state.placements.findIndex((elem)=>{   
            return elem.id == item.id;
        })

        if(index >= 0 || this.state.limit <= state.placements.length){     return;     }

        state.placements.push(item);
        this.props.parent.setState(state);

        state = this.state;
        index = state.suggestions.findIndex((elem)=>{    
            return elem.id == item.id;
        })

        if(index >=0 ){
            state.suggestions.splice(index,1);
            this.setState(state);
        }
    }

    getPlacementSuggestions(){
        if(this.state.name == ""){  return; }

        var component = this;
        var url = webUrl + "getPlacements/" + this.state.name.toLowerCase();
        var state = component.state;

        axios({
            url:url,
            method:"GET"
        }).then((response)=>{
            var data = response.data;
            switch (response.status) {
                case 200: {
                    state.suggestions = data.content;
                    component.setState(state);
                    break;
                }
            }
        }).catch((response) => {

            switch(response.status){
                case 404:{
                    component.props.main.state.errorPopup.displayError("Error accessing server. Please try again later.");
                    break;
                }
            }            
        })

    }

    render() {
        var placements = this.props.parent.state.placements;

        return (
            <div className="tagInput">
                {
                    placements.map((item, i) => {
                        return (<Placement tag={item} parent={this.props.parent} key={i} index={i}/>);
                    })
                }

                <div className={this.state.activeInput == true ? "tagInput__input--active" : "tagInput__input--disabled"}>
                    <div className="tagInput__input__name">
                        <input type="text" className="text_input_2 f_input_1" value={this.state.name} onChange={this.handleNameChange} />
                    </div>

                    <div className="tagInput__input__buttons">

                        <div className="tagInput__input__add">
                            <div className="iconBtn--normal" onClick={() => { this.toggleInput() }}>
                                <svg className="icon">
                                    <use xlinkHref="#add" />
                                </svg>
                            </div>
                        </div>
                        
                       
                        <div className="tagInput__input__cancel">
                            <div className="iconBtn--normal" onClick={() => { this.toggleInput() }}>
                                <svg className="icon">
                                    <use xlinkHref="#back" />
                                </svg>
                            </div>
                        </div>

                    </div>

                </div>

                <div className="tagInput__suggestions">
                    {
                        this.state.suggestions.map((item, i) => {
                            return (<div className="tagS f_normal f_text-capitalize" key={i} onClick={()=>{this.selectPlacement(item)}}>{item.name + " "+ item.surname + " " + item.code}</div>);
                        })
                    }
                </div>
            </div>
        );
    }
}


class Placement extends Component {
    constructor(props){
        super(props);

        this.removePlacement = this.removePlacement.bind(this);
    }

    removePlacement(){
        var state = this.props.parent.state;
        state.placements.splice(this.props.index,1);
        this.props.parent.setState(state);
    }

    render() {
        var tag = this.props.tag;
        var name = tag.name + " " + tag.surname;

        return (
            <div className="tag">
                <div className="tag__cancel">
                    <div className="iconBtn--white" onClick={() => { this.removePlacement() }}>
                        <svg className="icon">
                            <use xlinkHref="#close" />
                        </svg>
                    </div>
                </div>
                <div className="tag__name f_normal">{name.toUpperCase()}</div>
            </div>    
        );
    }
}

export default PlacementInput;