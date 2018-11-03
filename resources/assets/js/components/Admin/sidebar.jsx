import React, { Component } from 'react';
import {WEB_URL} from '../../abstract/variables';

class SideBar extends Component {
    render() {

        return (
            <div id="adminSideBarMenu">
            
                <div className="navMenu" >
                    <div className="navMenu__subMenu">
                        <a href={WEB_URL + 'admin/products'} >
                            <div className="navMenu__subMenu__hd f_tab_h1" id="hd1">Products</div>
                        </a>
                    </div>
                    
                    <div className="navMenu__subMenu">
                        <a href={WEB_URL + 'admin/accounts'} >
                            <div className="navMenu__subMenu__hd f_tab_h1 " id="hd1">Accounts</div>
                        </a>
                    </div>

                    <div className="navMenu__subMenu">
                        <a href={WEB_URL + 'admin/repo'} >
                            <div className="navMenu__subMenu__hd f_tab_h1" id="hd1">Repository</div>
                        </a>
                    </div>


                </div>
            </div>
        );
    }
}

export default SideBar;