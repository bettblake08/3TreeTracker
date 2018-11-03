import React, { Component } from 'react';
import { WEB_URL, MAIN_LOGO } from '../../abstract/variables';
import setSVGIcons from "../../abstract/icons";
import MenuType1 from '../UI/menuType1';

class MainHeader extends Component {
    constructor(props) {
        super(props);

        this.handleScroll = this.handleScroll.bind(this);
        this.togglePopupMenu = this.togglePopupMenu.bind(this);

        this.state = {
            toggleHeader: 0,
            togglePopupMenu: 0,
        }
    }

    componentDidMount() {
        document.getElementById('svg_icons').innerHTML = setSVGIcons();
        window.addEventListener('scroll', this.handleScroll);
    }

    componentWillUnmount() {
        window.removeEventListener('scroll', this.handleScroll);
    }

    handleScroll(e) {
        var offset = 2;
        var state = this.state;

        var scrollYpos = window.scrollY;

        if (scrollYpos > offset && state.toggleHeader == 0) {
            state.toggleHeader = 1;
            this.setState(state);

        }
        else if (scrollYpos < offset && state.toggleHeader == 1) {
            state.toggleHeader = 0;
            this.setState(state);
        }

    }

    togglePopupMenu(menu) {
        var state = this.state;
        state.togglePopupMenu = state.togglePopupMenu == menu ? 0 : menu;
        this.setState(state);
    }

    render() {
        var headerClass = " header container-fluid ";
        this.state.toggleHeader == 0 ? headerClass += "header--normal" : headerClass += "header--float";
        var popupMenu = "popupMenu";

        var menuLinks = [
            [
                {
                    url: WEB_URL + 'login',
                    text: 't-10'
                },
                {
                    url: WEB_URL + 'sign_up',
                    text: 't-55'
                }
            ]
        ];

        return (
            <div className={headerClass}>
                <div className="row">
                    <div className="header__left">
                        <a href={WEB_URL}>
                            <div className="header__logo">
                                <img src={MAIN_LOGO} />
                            </div>
                        </a>
                        <div className="header__title f_banner_1">Longrich</div>
                    </div>

                    <div className="header__right">
                        <div className="header__right__menuBtn btn_icon--normal" onClick={() => { this.togglePopupMenu(1) }}>
                            <svg className="icon">
                                <use xlinkHref="#menu" />
                            </svg>
                        </div>

                        <div className="header__right__text f_normal f_text-capitalize t-56"></div>


                    </div>
                </div>

                <div className={this.state.togglePopupMenu == 1 ? popupMenu + "--active" : popupMenu + "--disabled"}>
                    <div className="popupMenu__mainMenu">
                        <MenuType1 menu={menuLinks} opposite={true} />
                    </div>
                </div>

            </div>




        );
    }
}

export default MainHeader;