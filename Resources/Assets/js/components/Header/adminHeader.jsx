import React, { Component } from 'react';
import{ webUrl , setSVGIcons} from '../../abstract/variables';
import axios from 'axios';

class AdminHeader extends Component {
    constructor(props){
        super(props);

        this.retrieveData = this.retrieveData.bind(this);
        this.setData = this.setData.bind(this);
        this.reloadAjaxRequest = this.reloadAjaxRequest.bind(this);
        this.togglePopupMenu = this.togglePopupMenu.bind(this);

        this.state = {
            ajax:{
                retrieveData:{
                    attempts:0,
                    error:0
                }
            },
            seenCount:0
        }
    }

    componentWillMount(){
        //this.setData();
        document.getElementById("svg_icons").innerHTML = setSVGIcons();
    }

    setData() {
        var state = this.state;
        var profile = JSON.parse(localStorage.getItem('adminUser'));

        if (profile != null || profile != undefined) {
            return;
        }
        
        this.retrieveData();
    }

    retrieveData() {
        var component = this;
        var state = component.state;

        axios({
            url:webUrl + "admin/getData",
            method:"GET"
        }).then((response)=>{
            var data = response.data;

            switch (data.error) {
                case 0: {
                    var profile = JSON.parse(localStorage.getItem('adminUser'));

                    profile == undefined || profile == null ? profile = {} : null;

                    localStorage.setItem('adminUser', JSON.stringify(profile));
                    component.setData();
                    break;
                }
            }
        });

    };


    reloadAjaxRequest(option) {
        var state = this.state;

        switch (option) {
            case 1: {

                if (state.ajax.retrieveData.attempts < 10) {
                    state.ajax.retrieveData.attempts += 1;
                    this.setState(state);
                    this.retrieveData();
                }
                else {
                    state.ajax.retrieveData.error = "Access to server failed. Try again Later! ";
                    this.setState(state);
                }
                break;
            }
        }

    }

    togglePopupMenu(menu) {
        var state = this.state;
        state.togglePopupMenu = state.togglePopupMenu == menu ? 0 : menu;
        this.setState(state);
    }

    render() {

        return (
            <div className="header--active " style={{ margin: 0, padding: 0 }}>
                    <div className="header">
                        <div className="header__left">
                            <a href={webUrl + 'admin/home'}>
                                <div className="header__logo">
                                    <img src={webUrl + 'assets/images/edulink.png'} />
                                </div>
                            </a>
                        </div>

                        <div className="header__title f_banner_1 f_text-capitalize">Admin Platform</div>


                        <div className="header__right">
                            <div className="header__right__logOut">
                                <a href={webUrl + 'admin/logout'}>
                                    <div className="btn_1--danger f_button_2 f_text-capitalize">Logout</div>
                                </a>
                            </div>

                            <div className="header__right__nf btn_icon--normal" onClick={() => { this.togglePopupMenu(1) }}>
                                <svg className="icon">
                                    <use xlinkHref={"#note"} />
                                </svg>
                                <div className="btn_icon__number" style={this.state.seenCount == 0 ? { display: 'none' } : { display: 'block' }}>{this.state.seenCount}</div>
                            </div>

                        </div>



                    </div>

            </div>
        );
    }
}


export default AdminHeader;