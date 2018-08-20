import humanize from '@nlib/human-readable';
import axios from 'axios';
import jsPDF from 'jspdf';
import React, { Component } from 'react';
import Slider from "react-slick";
import {getCountries} from '../../abstract/country';
import webUrl from '../../abstract/variables';
import PlacementInput from '../placementInput';
import Button from '../UI/button';
import DateInput from '../UI/dateInput';
import DropdownInput from '../UI/dropdownInput';
import ErrorPopup from '../UI/errorPopup';
import { NewPasswordInput,PasswordInput } from '../UI/newPasswordInput';
import TextInput from '../UI/textInput';
import ViewProduct from './home/viewProduct';


class Home extends Component {
    constructor(props){
        super(props);

        this.state = {
            view:1,
            errorPopup:{}
        }

        this.setView = this.setView.bind(this);
    }

    setView(option){
        var state = this.state;
        state.view = option;
        this.setState(state);
    }

    render() {
        var viewClass = "view__options";
        viewClass += "--" + this.state.view;

        return (

            <div id="section_1">
                <ErrorPopup parent={this} />
                <div className={viewClass} >
                    <div className={view == 1 ? "view__option--active" : "view__option--disabled"} onClick={() => { this.setView(1) }} >
                        <svg className="icon">
                            <use xlinkHref="#menu" />
                        </svg>
                    </div>
                    <div className={view == 2 ? "view__option--active" : "view__option--disabled"} onClick={()=>{this.setView(2)}}>
                        <svg className="icon">
                            <use xlinkHref="#magnifier" />
                        </svg>
                    </div>
                    <div className={view == 3 ? "view__option--active" : "view__option--disabled"} onClick={() => { this.setView(3) }}>
                        <svg className="icon">
                            <use xlinkHref="#info" />
                        </svg>
                    </div>
                    <div className={view == 4 ? "view__option--active" : "view__option--disabled"} onClick={() => { this.setView(4) }}>
                        <svg className="icon">
                            <use xlinkHref="#note" />
                        </svg>
                    </div>
                </div>

                <div className={this.state.view == 1 ? "view--active" : "view--disabled"}>
                    <LandingView />
                </div>

                <div className={this.state.view == 2 ? "view--active" : "view--disabled"}>
                    <Products parent={this}/>
                </div>

                <div className={this.state.view == 3 ? "view--active" : "view--disabled"}>
                    <InfoView />
                </div>

                <div className={this.state.view == 4 ? "view--active" : "view--disabled"}>
                    <AccountView parent={this} />
                </div>

            </div>
        );
    }
}

class LandingView extends Component {
    render() {
        var settings = {
            dots: true,
            infinite: true,
            speed: 500,
            autoPlaySpeed:3000,
            slidesToShow: 1,
            slidesToScroll: 1,/* 
            nextArrow: <NextArrow />,
            prevArrow: <PrevArrow /> */
        };

        return (
            <Slider {...settings}>
                <div>
                    <div className="lview--1 lview">
                        <div className="lview__content">
                            <div className="lview__title f_title ">Cultivating the Future</div>
                            <div className="lview__body f_h1">
                                Welcome to the Edulink platform, providing a network for students, teachers and educational institutions such as universities, professional schools and high schools, to share resources, ideas and information concerning the field of learning.
                            </div>
                            <div className="lview__buttons">
                                <div className="lview__button">
                                    <a href={webUrl + 'login'}>
                                        <div className="btn_1--edulink f_button_2 t-10 f_text-capitalize"></div>
                                    </a>
                                </div>

                                <div className="lview__button">
                                    <a href={webUrl + 'sign_up'}>
                                        <div className="btn_1--edulink f_button_2 t-55 f_text-capitalize"></div>
                                    </a>
                                </div>
                            </div>
                        </div>
                       
                    </div>
                </div>

                <div>
                    <div className="lview--2 lview">
                        <div className="lview__content">

                            <div className="lview__title f_title ">A student can </div>
                            <div className="lview__body f_h1">
                                <ul>
                                    <li>Communicate and share resources with teachers and students.</li>
                                    <li>Keep up with the latest info from institutions, students and teachers</li>
                                    <li>Manage their student info</li>
                                    <li>View their grades</li>
                                    <li>View and manage their school schedule</li>
                                    <li>Perform reviews and ratings</li>
                                    <li>And much more ...</li>
                                </ul>


                            </div>

                        </div>


                        <div className="lview__buttons">
                            <div className="lview__button">
                                <a href={webUrl + 'login'}>
                                    <div className="btn_1--edulink f_button_2 t-10 f_text-capitalize"></div>
                                </a>
                            </div>

                            <div className="lview__button">
                                <a href={webUrl + 'sign_up'}>
                                    <div className="btn_1--edulink f_button_2 t-55 f_text-capitalize"></div>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>

                <div>
                    <div className="lview--3 lview">
                        <div className="lview__content">

                            <div className="lview__title f_title ">A teacher can </div>
                            <div className="lview__body f_h1">
                                <ul>
                                    <li>Manage their profile</li>
                                    <li>Communicate and share resources with teachers and students all over the world</li>
                                    <li>Keep up with the latest news from institutions, students and teachers</li>
                                    <li>Update and maintain student grades</li>
                                    <li>Execute attendance check</li>
                                    <li>And much more ...</li>
                                </ul>

                            </div>
                        </div>

                        <div className="lview__buttons">
                            <div className="lview__button">
                                <a href={webUrl + 'login'}>
                                    <div className="btn_1--edulink f_button_2 t-10 f_text-capitalize"></div>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>



                <div>
                    <div className="lview--4 lview">
                        <div className="lview__content">

                            <div className="lview__title f_title ">An institution can </div>
                            <div className="lview__body f_h1">

                                <li>Manage a personalized subdomain</li>
                                <li>Manage students and Teaching staff</li>
                                <li>Easily and seemlessly schedule class timetables</li>
                                <li>Post news feeds</li>
                                <li>Monitor attendance</li>
                                <li>Manage online student applications</li>
                                
                            </div>
                        </div>

                        <div className="lview__buttons">
                            <div className="lview__button">
                                <a href={webUrl + 'insAdmin/login'}>
                                    <div className="btn_1--edulink f_button_2 t-10 f_text-capitalize"></div>
                                </a>
                            </div>

                            <div className="lview__button">
                                <a href={webUrl + 'insAdmin/registration'}>
                                    <div className="btn_1--edulink f_button_2 t-55 f_text-capitalize"></div>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>




            </Slider>
        );
    }
}

class Products extends Component {
    constructor(props) {
        super(props);

        this.state = {
            view: 1,
            viewProduct: {},
            productsView: {}
        }

        this.setView = this.setView.bind(this);
    }

    setView(option) {
        var state = this.state;
        state.view = option;
        this.setState(state);
    }


    render() {

        return (
            <div className="SB">

                <div className={this.state.view == 1 ? "viewh--active" : "viewh--disabled"}>
                    <div className="view--scrollable">
                        <ProductsView parent={this} />
                    </div>
                </div>

                <div className={this.state.view == 2 ? "viewh--active" : "viewh--disabled"}>
                    <div className="view--scrollable">
                        <ViewProduct parent={this} />
                    </div>
                </div>

            </div>
        );
    }
}

class ProductsView extends Component {
    constructor(props) {
        super(props);

        var Viewable = {
            product: true,
            event: true,
            notice: true
        };

        this.state = {
            viewable: Viewable,
            content: [],
            offset: 0,
            buttons: [],
            viewType: {
                product: 1,
                event: 1,
                notice: 1
            }
        }

        this.getProducts = this.getProducts.bind(this);
    }

    componentDidMount() {
        this.getProducts();
    }

    getProducts(reset = false) {
        var c = this;
        var state = c.state;
        var errorPopup = this.props.parent.props.parent.state.errorPopup;
        if (reset) {
            state.offset = 0;
            state.content = [];
        }

        axios({
            url: webUrl + "admin/getProducts/" + state.offset,
            method: "GET"
        }).catch((response) => {

            switch (response.status) {
                case 202: {
                    break;
                }
                default: {
                    setTimeout(() => {
                        c.getProducts();
                    }, 1000)
                    break
                }
            }

        }).then((response) => {
            var data = response.data;

            switch (data.error) {
                case 0: {

                    if (data.content.length == 0) {
                        errorPopup.displayError("There are no more products to retrieve. Continue creating more.");
                        break;
                    }

                    state.content = state.content.concat(data.content);
                    state.offset += data.content.length;
                    c.setState(state);
                    break;
                }
            }
        })

    }

    render() {
        var c = this;
        return (
            <div id="content">
                <div className="content__view">

                    {
                        this.state.content.map((item, i) => {
                            switch (item.log.type) {
                                case 1: {
                                    if (!this.state.viewable.product) { return; }

                                    switch (this.state.viewType.product) {
                                        case 1: { return (<div className="pro" key={i}><Product post={item} parent={this} /></div>); }
                                    }

                                    break;
                                }
                            }
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
                            action: () => {
                                c.getProducts()
                            }
                        }} />
                </div>
            </div>
        );
    }
}

class Product extends Component {
    render() {
        var post = this.props.post;
        var parent = this.props.parent.props.parent;

        const image = {
            background: 'url("' + webUrl + "repo/" + post.post.image.name + '/thumb_150_150.jpg")',
            backgroundPosition: 'center',
            backgroundSize: 'cover'
        }


        return (
            <div className="pro--1__con" id={"p-" + post.log.id}>
                <div className="pro--1__con__up" style={image}
                    onClick={
                        () => {
                            parent.setView(2)
                            parent.state.viewProduct.state.product.id = post.post.id;
                            parent.state.viewProduct.getProduct();
                        }}>
                        
                    <div className="pro--1__link">
                        <div className="pro--1__title f_normal f_text-capitalize">{post.post.title}</div>
                        <svg className="icon">
                            <use xlinkHref="#view" />
                        </svg>
                    </div>


                </div>

                <div className="pro--1__con__down">

                    <div className="pro--1__stat">
                        <div className="pro--1__stat__view">
                            <div className="pro--1__stat__icon">
                                <div className="iconBtn--normal">
                                    <svg className="icon">
                                        <use xlinkHref="#view" />
                                    </svg>
                                </div>
                            </div>
                            <div className="pro--1__stat__value f_h2 f_text-bold">{humanize(post.post.stat.views)}</div>
                        </div>

                        <div className="pro--1__stat__likes">
                            <div className="pro--1__stat__icon">
                                <div className="iconBtn--normal">
                                    <svg className="icon">
                                        <use xlinkHref="#like" />
                                    </svg>
                                </div>
                            </div>
                            <div className="pro--1__stat__value f_h2 f_text-bold">{humanize(post.post.stat.reactions)}</div>
                        </div>

                        <div className="pro--1__stat__com">
                            <div className="pro--1__stat__icon">
                                <div className="iconBtn--normal">
                                    <svg className="icon">
                                        <use xlinkHref="#communication" />
                                    </svg>
                                </div>
                            </div>
                            <div className="pro--1__stat__value f_h2 f_text-bold">{humanize(post.post.stat.comments)}</div>
                        </div>


                    </div>
                </div>
            </div>
        );
    }
}

class InfoView extends Component {
    render() {
        return (
            <div className="infoView SB">
                <div className="infoView__content">
                    <div className="infoView__1">
                        <div className="infoView__1__title f_title f_text-center">Want your institution to have an online presence?</div>
                        <div className="infoView__1__text f_h2 f_text-center">
                            From a personalized website, to a management system that easy and affordable to integrate according to the size of your institution, our platform is capable of providing the technological edge your institution needs.
                        </div>
                    </div>

                
                    <div className="infoView__2">
                        <div className="infoBox">
                            <div className="infoBox__icon">
                                <svg className="icon">
                                    <use xlinkHref="#lock-2" />
                                </svg>
                            </div>
                            <div className="infoBox__title f_h1 f_text-center">Secure</div>
                            <div className="infoBox__text f_h2 f_text-center">We offer a secure software solution for educational institutions to store and process important data concerrning the institution.</div>
                        </div>

                        <div className="infoBox">
                            <div className="infoBox__icon">
                                <svg className="icon">
                                    <use xlinkHref="#business" />
                                </svg>
                            </div>
                            <div className="infoBox__title f_h1 f_text-center">Reliable</div>
                            <div className="infoBox__text f_h2 f_text-center">We strive to offer a quality software solution that is available 24/7. Any maintenance routines is pre-informed before execution.</div>
                        </div>

                        <div className="infoBox">
                            <div className="infoBox__icon">
                                <svg className="icon">
                                    <use xlinkHref="#responsive-devices" />
                                </svg>
                            </div>
                            <div className="infoBox__title f_h1 f_text-center">Responsive</div>
                            <div className="infoBox__text f_h2 f_text-center">We offer a software solution that scales seemlessly across desktop and mobile devices.
                        </div>
                        </div>

                    </div>



                    <div className="infoView__3">
                        <div className="infoView__3__title f_title f_text-center">Register now for a 7 day trial.</div>
                        <div className="infoView__3__text f_h2 f_text-center">
                            Start integration in seconds. Develop an online presence in minutes.
                        </div>
                        <div className="infoView__3__buttons">
                            <div className="lview__button">
                                <a href={webUrl + 'insAdmin/registration'}>
                                    <div className="btn_1--white f_button_2 f_text-capitalize">Get Started</div>
                                </a>
                            </div>
                        </div>
                    </div>



                    <div className="infoView__1">
                        <div className="infoView__1__title f_title f_text-center">Starter Packages</div>
                        <div className="infoView__1__text f_h2 f_text-center">Edulink charges institutions registered to the platform according to the number of students enrolled using the platform (KES200 per student). We have the following starter packages available for newcomers that help you get started.</div>
                    </div>


                    <div className="infoView__2">

                       

                        <div className="infoBox">
                            <div className="infoBox__title f_h1 f_text-center">Basic</div>
                            <div className="infoBox__text f_h2 f_text-center">
                                A starter package for a low funded educational institution</div>
                            <div className="infoBox__list f_h2">
                                <ul>
                                    <li>Enroll 100 students free</li>
                                    <li>1 GB repository space</li>
                                    <li>A free personalized website</li>
                                </ul>
                            </div>  
                            <div className="infoBox__text f_comment_1">
                                Note: This is a one time payment. After exceeding the number of students you can enroll for free, you shall resume to the standard fee for student enrollment billed per month. ( 200 KSH per student) 
                            </div>    
                            <div className="infoBox__price f_normal f_text-center">
                                Only <strong className="f_h1" >10000 KSH</strong>
                            </div>                  
                        </div>


                        <div className="infoBox">
                            <div className="infoBox__title f_h1 f_text-center">Standard</div>
                            <div className="infoBox__text f_h2 f_text-center">
                                A Standard package for a well funded educational institution</div>
                            <div className="infoBox__list f_h2">
                                <ul>
                                    <li>Enroll 200 students free</li>
                                    <li>1 GB repository space</li>
                                    <li>A free personalized website</li>
                                </ul>
                            </div>
                            <div className="infoBox__text f_comment_1">
                                Note: This is a one time payment. After exceeding the number of students you can enroll for free, you shall resume to the standard fee for student enrollment billed per month. ( 200 KSH per student)
                            </div>
                            <div className="infoBox__price f_normal f_text-center">
                                Only <strong className="f_h1" >20000 KSH</strong>
                            </div>
                        </div>




                        <div className="infoBox">
                            <div className="infoBox__title f_h1 f_text-center">Premium</div>
                            <div className="infoBox__text f_h2 f_text-center">A premium package for a well established and funded educational institution</div>
                            <div className="infoBox__list f_h2">
                                <ul>
                                    <li>Enroll 500 students free</li>
                                    <li>1 GB repository space</li>
                                    <li>A free personalized website</li>
                                </ul>
                            </div>
                            <div className="infoBox__text f_comment_1">
                                Note: This is a one time payment. After exceeding the number of students you can enroll for free, you shall resume to the standard fee for student enrollment billed per month. ( 200 KSH per student)
                            </div>
                            <div className="infoBox__price f_normal f_text-center">
                                Only <strong className="f_h1" >40000 KSH</strong>
                            </div>
                        </div>

                    </div>



                </div>
            </div>
        );
    }
}

class AccountView extends Component {
    render() {
        return (
           <div className="accountView">
                <AccountLogin parent={this.props.parent}/>
                <AccountRegistration parent={this.props.parent} />
           </div>
        );
    }
}

class AccountLogin extends Component {
    constructor(props) {
        super(props);

        this.userLogin = this.userLogin.bind(this);

        this.state = {
            error: 0,
            buttons:[],
            passwordInputs: [],
            textInputs:[]
        }
    }

    componentDidUpdate() {
        if (this.state.error != 0) {
            setTimeout(() => {
                var state = this.state;
                state.error = 0;
                this.setState(state);
            }, 3000);
        }
    }

    userLogin() {
        var component = this;
        var state = this.state;
        var usernameType = 0;
        var username = this.state.username;

        var emailRegex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

        if(username == ""){
            state.textInputs[0].state.errorText = "Incorrect input value. Please input an email or account code.";
            state.textInputs[0].state.status = 1;
            component.setState(state);
            return;
        }
        else if (emailRegex.test(String(username).toLowerCase())) { usernameType = 1; }
        else { usernameType = 2; }

        state.buttons[0].state.status = 3;
        component.setState(state);

        axios({
            url: webUrl + 'admin/loginAuth',
            method:"POST",
            data: {
                usernameType:usernameType,
                username: username,
                password: password
            }
        }).then((response)=>{
            var data = response.data;
            console.log("Log in successful! Error:" + data.error);

            switch (data.error) {
                case 0: {
                    window.location.href = webUrl + "admin/products";
                    break;
                }
                case 1:
                case 2:
                case 3:{
                    state.error = data.data.error;
                    state.buttons[0].state.status = 1;
                    component.setState(state);
                    break;
                }
            }
        }).catch((response)=>{
            if(response.status != 200){
                state.error = 404;
                component.setState(state);
            }
        })

    };


    render() {

        var errorText = "";

        switch (this.state.error) {
            case 1: {
                errorText = "User doesn't exist. Please enter a valid username";
                break;
            }
            case 2:
            case 3:{
                errorText = "Username or password is incorrect. Please try again.";
                break;
            }
            case 404: {
                errorText = "Access to server failed. Please try again. ";
                break;
            }
        }

        return (
            <div className="loginForm view--scrollable SB">
                <div className="loginForm__form">
                    <form method="post">
                        <h1 className="f_title">Account Login.</h1>
                        <h2 className="f_h2">
                        If this is your first time, please provide a Longrich account code provided by Longrich. If not, you may ingore.</h2>
                        <div className="loginForm__code">
                            <TextInput
                                parent={this}
                                status={0}
                                config={{
                                    text: "",
                                    floatingLabel: true,
                                    label: "Code",
                                    type: "text_input_4",
                                    placeholder: "Account Code",
                                    length: 60,
                                    comment: "Maximum characters allowed is (60)."
                                }} />

                        </div>          

                        <h2 className="f_h2">The following details are required.</h2>

                        <div className="loginForm__username">
                            <TextInput
                                parent={this}
                                status={0}
                                config={{
                                    text: "",
                                    floatingLabel: true,
                                    label: "Account",
                                    type: "text_input_4",
                                    placeholder: "Email Address / Account Code",
                                    length: 60,
                                    comment: "Maximum characters allowed is (60)."
                                }} />

                        </div>

                        <div className="loginForm__pass" >
                            <PasswordInput
                                parent={this}
                                status={0}
                                config={{
                                    class: "text_input_4",
                                    floatingLabel: true,
                                    label: "Password",
                                    placeholder: "At least 1 of each (A-Z),(a-z),(1-9),(@$.#). 8-16 characters."
                                }} />
                        </div>

                        <div className="loginForm__errorComment" className={this.state.error != 0 ? "errorComment--active f_comment_1" : "errorComment--disabled f_comment_1"}>
                            {errorText}
                        </div>

                        <div className="loginForm__btn">
                            <Button 
                                parent={this} 
                                status={0} 
                                config={{ 
                                    text: "",
                                    label: "Log In", 
                                    type: "btn_1", 
                                    action: this.userLogin 
                                }} 
                             />
                        </div>


                    </form>
                </div>
            </div>

        );
    }
}


class AccountRegistration extends Component {
    constructor(props) {
        super(props);
        this.state = {  
            textInputs:[],
            dateInputs:[],
            dropdownInputs:[],
            newPasswordInput:{},
            placements:[],
            buttons:[],
            placement:{},
            view:1
        };

        this.register = this.register.bind(this);
        this.getPDF = this.getPDF.bind(this);
        this.savetoPDF = this.savetoPDF.bind(this);
        this.setView = this.setView.bind(this);
    }

    componentDidMount(){
        this.getPDF();
    }

    setView(view){
        var state = this.state;
        state.view = view;
        this.setState(state);
    }

    getPDF(){
        var longrichForm = localStorage.getItem("longrichForm");

        if(longrichForm!= undefined){
            return;
        }
        else {
            var errorPopup = this.props.parent.state.errorPopup;

            axios({
                url: webUrl + "getForm",
                method: "GET"
            }).then((response) => {
                var data = response.data;

                switch (data.error) {
                    case 0: {
                        localStorage.setItem('longrichForm',data.content);
                        return;
                    }
                }
            }).catch((response) => {
                if(response.status != 200){
                    errorPopup.displayError("Failed to access server. Please try again in a few minutes.");
                }
            })
        }
    }

    savetoPDF(){
        var textInputs = this.state.textInputs;
        var dateInputs = this.state.dateInputs;
        var dropdownInputs = this.state.dropdownInputs;
        var c = this;

        var found = textInputs.concat(dateInputs,dropdownInputs).find((elem) => {
            return elem.state.inputValue == "";
        })

        if(found != undefined){
            c.setView(1);
            found.focus()
            return;
        } 

        var doc = new jsPDF();
        var imgData = localStorage.getItem("longrichForm");

        if(imgData == undefined){
            this.props.parent.state.errorPopup.displayError("Failed to generate PDF version of form. Try again in a mintue.");
            return;
        }

        doc.addImage(imgData, 'JPEG', 0, 0, 210, 297);

        doc.setFontSize(16);
        doc.setTextColor(0, 0, 0);

        var x = 58;
        var c = 16;

        var placement = this.state.placement;
  
        doc.text(115, x + (c * 0), textInputs[0].state.inputValue);
        doc.text(115, x + (c * 1), textInputs[1].state.inputValue);
        doc.text(115, x + (c * 2), textInputs[2].state.inputValue);
        doc.text(115, x + (c * 3), dropdownInputs[0].state.inputValue == 0 ? "Male" : "Female");
        doc.text(115, x + (c * 4), dateInputs[0].state.inputValue);
        doc.text(115, x + (c * 5), textInputs[3].state.inputValue);
        doc.text(115, x + (c * 6), textInputs[4].state.inputValue);
        doc.text(115, x + (c * 7), textInputs[5].state.inputValue);
        doc.text(115, x + (c * 8), textInputs[6].state.inputValue);
        doc.text(115, x + (c * 9), textInputs[7].state.inputValue);
        doc.text(115, x + 6 + (c * 10), textInputs[8].state.inputValue + " - " + textInputs[9].state.inputValue);
        doc.text(115, x + 6 +(c * 11), textInputs[10].state.inputValue + " - " + textInputs[11].state.inputValue);
        doc.text(115, x + 6 + (c * 12), placement.name + " " + placement.surname + " " +  placement.code);
        

        doc.save('Longrich-Form' + '.pdf');
    }

    register(){
        var textInputs = this.state.textInputs;
        var dateInputs = this.state.dateInputs;
        var dropdownInput = this.state.dropdownInputs;
        var newPasswordInput = this.state.newPasswordInput;

        textInputs.forEach((elem) => {
            if (elem.state.inputValue == "") {
                elem.focus();
                return;
            }
        })

        dateInputs.forEach((elem) => {
            if (elem.state.inputValue == "") {
                elem.focus();
                return;
            }
        })

        dropdownInput.forEach((elem) => {
            if (elem.state.inputValue == "") {
                elem.focus();
                return;
            }
        })

        if(newPasswordInput.state.inputValue == ""){
            newPasswordInput.focus();
            return;
        }

        var formData = {
            name:textInputs[0].state.inputValue,
            surname:textInputs[1].state.inputValue,
            email:textInputs[4].state.inputValue,
            phoneNo: textInputs[5].state.inputValue,
            gender: dropdownInput[0].state.inputValue,
            nationality:dropdownInput[1].state.inputValue,
            password: newPasswordInput.state.inputValue,
            placement: this.state.placements[0].id
        }


        var errorPopup = this.props.parent.state.errorPopup;
        var c = this;

        axios({
            url: webUrl + "longrichAccount",
            method: "POST",
            data: formData
        }).then((response) => {
            var data = response.data;

            switch (data.error) {
                case 0: {
                    state.placement = data.content.placement;
                    c.setState(state);
                    c.setView(2);
                    break;
                }
                case 1: {
                    errorPopup.displayError("Failed to register you into the system. Please try again");
                    break;
                }
            }
        }).catch((response) => {
            if(response.status != 200){
                errorPopup.displayError("Failed to access server. Please try again in a few minutes.");
            }
        })

    }


    render() {
        var view = this.state.view;
        var countries = [];

        var cs = getCountries();
        
        cs.forEach((n)=>{
            countries.push({
                value:n.Code,
                label:n.Name
            })
        })

        return (
            <div className="regView">
                <div className={view == 1 ? "viewh--active" : "viewh--disabled"}>
                    <div className="regView__view view--scrollable SB">
                        <form method="post" encType="multipart/form-data">

                            <div className="reg__form" >

                                <h1 className="f_title">Create an account now.</h1>
                                <h2 className="f_h2">Fill in the form below to register, then download the pdf version offered after completion.</h2>
                                <div className="reg__text">
                                    <TextInput
                                        parent={this}
                                        status={0}
                                        config={{
                                            text: "",
                                            floatingLabel: true,
                                            label: "Name",
                                            type: "text_input_4",
                                            length: 80,
                                            placeholder:"Firstname Middle Names",
                                            comment: "Maximum characters allowed is (80)."
                                        }} />
                                </div>

                                <div className="reg__text">
                                    <TextInput
                                        parent={this}
                                        status={0}
                                        config={{
                                            text: "",
                                            floatingLabel: true,
                                            label: "Surname",
                                            type: "text_input_4",
                                            length: 80,
                                            placeholder:"Surname",
                                            comment: "Maximum characters allowed is (80)."
                                        }} />
                                </div>

                                <div className="reg__text">
                                    <TextInput
                                        parent={this}
                                        status={0}
                                        config={{
                                            text: "",
                                            floatingLabel: true,
                                            label: "ID",
                                            type: "text_input_4",
                                            length: 80,
                                            placeholder: "National ID /Passport",
                                            comment: "Maximum characters allowed is (80)."
                                        }} />
                                </div>

                                <div className="reg__dd">
                                    <DropdownInput
                                        parent={this}
                                        status={0}
                                        config={{
                                            label: "Gender",
                                            floatingLabel: true,
                                            class: "dropdown_2",
                                            placeholder:"-- Select Gender -- ",
                                            options: [
                                                {
                                                    value: 0,
                                                    label: "Male"
                                                },
                                                {
                                                    value: 1,
                                                    label: "Female"
                                                },
                                            ]
                                        }}
                                    />
                                </div>

                                <div className="reg__dd">
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

                                <div className="reg__date">
                                    <DateInput
                                        parent={this}
                                        status={0}
                                        config={{
                                            text: "",
                                            floatingLabel:true,
                                            label: "Date of Birth",
                                            class: "text_input_4"
                                        }}
                                    />
                                </div>

                                <div className="reg__text">
                                    <TextInput
                                        parent={this}
                                        status={0}
                                        config={{
                                            text: "",
                                            floatingLabel: true,
                                            label: "Address",
                                            type: "text_input_4",
                                            placeholder: "Postal Address",
                                            length: 120,
                                            comment: "Maximum characters allowed is (120)."
                                        }} />
                                </div>

                                <div className="reg__text">
                                    <TextInput
                                        parent={this}
                                        status={0}
                                        config={{
                                            text: "",
                                            floatingLabel: true,
                                            label: "Email Address",
                                            type: "text_input_4",
                                            placeholder: "Email Address",
                                            length: 60,
                                            comment: "Maximum characters allowed is (60)."
                                        }} />
                                </div>

                                <div className="reg__text">
                                    <TextInput
                                        parent={this}
                                        status={0}
                                        config={{
                                            text: "",
                                            floatingLabel: true,
                                            label: "Phone number",
                                            type: "text_input_4",
                                            placeholder: "Mobile number",
                                            length: 60,
                                            comment: "Maximum characters allowed is (60)."
                                        }} />
                                </div>

                                <div className="reg__text">
                                    <TextInput
                                        parent={this}
                                        status={0}
                                        config={{
                                            text: "",
                                            floatingLabel: true,
                                            label: "Bank Name",
                                            type: "text_input_4",
                                            placeholder: "Bank name",
                                            length: 60,
                                            comment: "Maximum characters allowed is (60)."
                                        }} />
                                </div>

                                <div className="reg__text">
                                    <TextInput
                                        parent={this}
                                        status={0}
                                        config={{
                                            text: "",
                                            floatingLabel: true,
                                            label: "Bank Account",
                                            type: "text_input_4",
                                            placeholder: "Number, Name, Branch",
                                            length: 60,
                                            comment: "Maximum characters allowed is (60)."
                                        }} />
                                </div>

                                <div className="reg__text">
                                    <TextInput
                                        parent={this}
                                        status={0}
                                        config={{
                                            text: "",
                                            floatingLabel: true,
                                            label: "Beneficiary Name",
                                            type: "text_input_4",
                                            placeholder: "Full Name",
                                            length: 60,
                                            comment: "Maximum characters allowed is (60)."
                                        }} />
                                </div>

                                <div className="reg__text">
                                    <TextInput
                                        parent={this}
                                        status={0}
                                        config={{
                                            text: "",
                                            floatingLabel: true,
                                            label: "Beneficiary Number",
                                            type: "text_input_4",
                                            placeholder: "Mobile number",
                                            length: 60,
                                            comment: "Maximum characters allowed is (60)."
                                        }} />
                                </div>


                                <div className="reg__text">
                                    <TextInput
                                        parent={this}
                                        status={0}
                                        config={{
                                            text: "",
                                            floatingLabel: true,
                                            label: "Sponsor Name",
                                            type: "text_input_4",
                                            placeholder: "Full Name",
                                            length: 60,
                                            comment: "Maximum characters allowed is (60)."
                                        }} />
                                </div>

                                <div className="reg__text">
                                    <TextInput
                                        parent={this}
                                        status={0}
                                        config={{
                                            text: "",
                                            floatingLabel:true,
                                            label: "Sponsor Number",
                                            type: "text_input_4",
                                            placeholder: "Mobile number",
                                            length: 60,
                                            comment: "Maximum characters allowed is (60)."
                                        }} />
                                </div>

                                <div className="reg__placement">
                                    <div className="reg__placement__label f_h1">Recruited by: </div>
                                    <div className="reg__placement__input" >
                                        <PlacementInput main={this.props.parent} parent={this} limit={1} />
                                    </div>
                                    <div className="reg__placement__comment f_normal">Select a longrich agent to register under.<br/>The system shall use this agent to retrieve a placement under him/her.</div>
                                </div>

                                <div className="reg__password">
                                    <NewPasswordInput
                                        parent={this}
                                        regex={/^((?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@\$\.#]).{8,16})$/}
                                        config={{
                                            placeholder: "At least 1 of each (A-Z),(a-z),(1-9),(@$.#). 8-16 characters."
                                        }}
                                    />
                                </div>


                                <div className="reg__save">
                                    <Button parent={this} status={0} config={{
                                        label: "Register",
                                        action: this.register,
                                        type: "btn_1",
                                        text: ""
                                    }} />
                                </div>

                            </div>
                        </form>

                    </div>
                   
                </div>



                <div className={view == 2 ? "viewh--active" : "viewh--disabled"}>
                    <div className="reg__completed">
                            <h1 className="f_h1">You've successfully registered!</h1>
                            <h2 className="f_h2">
                                Please download a copy of your pdf form to register at the nearest Longrich Office.
                            </h2>
                            <div className="reg__completed__buttons">
                                <div className="reg__completed__button">
                                    <Button parent={this} status={0} config={{
                                        label: "Form",
                                        action: this.savetoPDF,
                                        type: "btn_1",
                                        text: ""
                                    }} />
                                </div>

                                <div className="reg__completed__button">
                                    <Button parent={this} status={0} config={{
                                        label: "Home",
                                        action: ()=>{
                                            window.location.href = "/";
                                        },
                                        type: "btn_1",
                                        text: ""
                                    }} />
                                </div>
                                
                            </div>
                        </div>
                </div>
            </div>
        );
    }
}

export default Home;