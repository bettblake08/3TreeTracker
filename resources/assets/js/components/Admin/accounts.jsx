import axios from 'axios';
import React, { Component } from 'react';
import { getCountries, getCountry } from "../../abstract/country";
import { webUrl } from '../../abstract/variables';
import PlacementInput from '../placementInput';
import Button from "../UI/button";
import ErrorPopup from '../UI/errorPopup';
import IconButton from '../UI/iconButton';
import Popup from '../UI/popup';
import TextInput from '../UI/textInput';
import DropdownInput from "../UI/dropdownInput";

class AccountsView extends Component {
    constructor(props) {
        super(props);

        var Viewable = {
            account:true,
            event: true,
            notice: true
        };

        this.state = {
            viewable:Viewable,
            content:[],
            offset:0,
            filterSearch:{
                name:"0",
                country:"0",
            },
            accountInFocus:{},
            viewType: {
                account: 1,
                event: 1,
                notice: 1
            },
            popups:[],
            errorPopup:{},
            buttons:[],
            textInputs:[],
            dropdownInputs:[],
            loaded:false,
            editAccountPopup:{}
        }

        this.getAccounts = this.getAccounts.bind(this);
        this.toggleEditAccountPopup = this.toggleEditAccountPopup.bind(this);
        this.loadEditAccountPopup = this.loadEditAccountPopup.bind(this);
    }

    componentDidMount(){
        var state = this.state;
        state.loaded = true;
        this.setState(state);

        this.getAccounts();
    }

    getAccounts(reset = false) {
        var c = this;
        var state = c.state;

        if(reset){
            state.offset = 0;
            state.content = [];
        }

        axios({
            url: webUrl + "admin/getAccounts/" + state.filterSearch.name + "/" + state.filterSearch.country + "/" + state.offset,
            method:"GET"
        }).then((response) => {
        
            if(response.status == 200){
                var data = response.data;

                if (data.content.length == 0) {
                    state.errorPopup.displayError("There are no more accounts to retrieve. Continue creating more.");
                    return;
                }

                state.content = state.content.concat(data.content);
                state.offset += data.content.length;
                c.setState(state);
            }

        }).catch((response) => {

            if(response.status != 200){
                setTimeout(() => {
                    c.getAccounts();
                }, 1000)
            }

        })

    }

    toggleEditAccountPopup() {
        this.state.popups[0].toggleContent();
    }

    loadEditAccountPopup() {
        if (this.state.loaded == true) {
            return (<Popup component={<EditAccountPopup parent={this} />} parent={this} />);
        }
    }

    render() {
        var main = this;
        var countries = [];

        getCountries().forEach((n) => {
            countries.push({
                value: n.Code,
                label: n.Name
            })
        })

        return (
            <div id="section_1" className="SB">

                <div id="content">
                    <ErrorPopup parent={this} />
                    {this.loadEditAccountPopup()}

                    <div className="topBar">
                        <div className="topBar__title f_h1">Accounts</div>
                        <div className="topBar__searchBar">
                            <TextInput
                                parent={this}
                                status={0}
                                config={{
                                    text: "",
                                    floatingLabel: true,
                                    label: "Name",
                                    type: "text_input_4",
                                    placeholder: "Firstname / Surname",
                                    length: 30
                                }} />
                        </div>

                        <div className="topBar__searchBar">
                            <DropdownInput
                                parent={this}
                                status={0}
                                config={{
                                    floatingLabel: true,
                                    label: "Nationality",
                                    class: "dropdown_2",
                                    placeholder: "-- Select Nationality -- ",
                                    options: countries
                                }}
                            />
                        </div>

                        <div className="topBar__searchBtn">
                            <Button
                                parent={this}
                                status={0}
                                config={{
                                    type: "btn_1",
                                    label: "Filter",
                                    text: "",
                                    action: () => {
                                        var state = main.state;
                                        var n = state.textInputs[0].state.inputValue;
                                        var c = state.dropdownInputs[0].state.inputValue;
                                        state.filterSearch.name = n != "" ? n : "0";
                                        state.filterSearch.country = c != "" ? c : "0";
                                        c.setState(state);
                                        c.getAccounts(true);
                                    }
                                }} />
                        </div>

                    </div>

                    <div className="content__view">
                        {
                            this.state.content.map((item, i) => {
                                return <Account account={item.account} key={i} parent={this} />;
                            })
                        }
                    </div>

                    <div className="loadBtn">
                        <Button
                            parent={this}
                            status={0}
                            config={{
                                type: "btn_1",
                                label: "More",
                                text: "",
                                action: this.getAccounts
                            }} />
                    </div>
                </div>

            </div>

        );
    }
}


class Account extends Component {
    constructor(props) {
        super(props);

        this.state = {
            ajax: {
                setAppStatus: {
                    attempts: 0,
                    error: ""
                }
            },
            iconButtons:[],
            toggleButtons: this.props.account.status != null ? true : false
        }

        this.getGender = this.getGender.bind(this);
    }

    getGender() {
        return this.props.account.gender == 0 ? "M" : "F";
    }

    render() {
        var account = this.props.account;
        if (account == undefined) { return <div></div>; }

        var parent = this.props.parent;
        var placement = account.placementId == 0 ? "None" : account.placement.name + " " + account.placement.surname;

        return (
            <div className="account">
                <div className="account__title f_normal ">{account.name + " " + account.surname}</div>
                <div className="account__gender f_normal f_text-center">{this.getGender()}</div>
                <div className="account__nation f_normal f_text-center">{account.nationality}</div>
                <div className="account__email f_normal f_text-center">{account.email}</div>
                <div className="account__phoneNo f_normal f_text-center">{account.phoneNo}</div>
                <div className="account__code f_normal f_text-center">{account.code}</div>
                <div className="account__placement f_normal f_text-center">{placement}</div>
                <div className={account.verified ? "account__verified--t f_normal f_text-center" : "account__verified--f f_normal f_text-center"}>{account.verified ? "True" : "False"}</div>

                <div className="account__buttons">

                    <div className="account__buttons__button">
                        <IconButton 
                            parent={this} 
                            status={0} 
                            config={{
                            action: ()=>{
                                parent.toggleEditAccountPopup();
                                parent.state.accountInFocus = account;
                                parent.state.editAccountPopup.state != undefined ? parent.state.editAccountPopup.setInput() : null;
                            },
                            class: "iconBtn",
                            icon:"edit"
                        }} />
                        
                    </div>

                </div>
            </div>
        );
    }
}


class EditAccountPopup extends Component {
    constructor(props) {
        super(props);

        this.state = {
            placements:[],
            buttons:[]
        }

        this.confirm = this.confirm.bind(this);
        this.setInput = this.setInput.bind(this);
    }

    componentDidMount(){
        var state = this.props.parent.state;
        state.editAccountPopup = this;
        this.props.parent.setState(state);

        this.setInput();
    }

    setInput(){
        var account = this.props.parent.state.accountInFocus;
        var state = this.state;
        account.placement == undefined ? null : state.placements.push(account.placement);
        this.setState(state);
    }

    confirm() {
        var c = this;
        var state = c.state;

        axios({
            url: webUrl + "admin/longrichAccount/" + state.offset,
            method: "PUT",
            data:{
                placementId:state.placements[0].id
            }
        }).then((response) => {

            if(response.status == 200){
                c.props.parent.toggleEditAccountPopup();
            }

        }).catch((response) => {

            switch (response.status) {
                case 404: {
                    state.errorPopup.displayError("There is no such user with this id. Please use vaild id.");
                    break;
                }
                case 500: {
                    state.errorPopup.displayError("Failed to save changes. Please try again later.");
                    break;
                }
                default: state.errorPopup.displayError("Failed to access server. Please try again later.");break;
            }

        })  
    }

    render() {
        console.log(this.state);

        return (
            <div className="editPP">
                <div className="editPP__content">
                    <form method="post" encType="multipart/form-data">

                        <div className="reg__form" >

                            <h1 className="f_h1">Edit Account Information</h1>

                            <div className="reg__placement">
                                <div className="reg__placement__label f_h1">Placement</div>
                                <div className="reg__placement__input" >
                                    <PlacementInput main={this.props.parent} parent={this} limit={1} />
                                </div>
                                <div className="reg__placement__comment f_comment_1">Select a longrich agent to register under.</div>
                            </div>

                        </div>
                    </form>
                </div>

                <div className="editPP__buttons">
                    <div className="editPP__buttons__button">
                        <Button
                            parent={this}
                            status={5}
                            config={{
                                type: "btn_1",
                                label: "Cancel",
                                text: "",
                                action: this.props.parent.toggleEditAccountPopup
                            }} />
                    </div>

                    <div className="editPP__buttons__button">
                        <Button
                            parent={this}
                            status={6}
                            config={{
                                type: "btn_1",
                                label: "Confirm",
                                text: "",
                                action: this.confirm
                            }} />
                    </div>

                </div>
            </div>
        );
    }
}

export default AccountsView;