import React, { Component } from 'react';
import {webUrl, defaultProductCoverPic} from '../../../abstract/variables';
import CommentingSystem from '../../commentingSystem';
import ErrorPopup from "../../UI/errorPopup";
import moment from "moment";
import axios from "axios";
import StickyBox from 'react-sticky-content';
import ButtonWithIcon from '../../UI/buttonWithIcon';

class ViewProduct extends Component {
    constructor(props){
        super(props);

        this.state = {
            userId:"",
            coverPhotoUrl:'',
            reaction:0,
            stat:{
                likes:0,
                dislikes:0
            },
            errorPopup:{},
            buttons:[],
            product:{
                id:this.props.productId,
                data:{},
            },
            commentingSystem:{},
            ajax:{
                retrieveProfileData:{
                        attempts:0,
                },
                getProduct: {
                    attempts: 0
                }
            }
        };

        this.reloadAjaxRequest = this.reloadAjaxRequest.bind(this);
        this.setCoverPhoto = this.setCoverPhoto.bind(this);
        this.reactToProduct = this.reactToProduct.bind(this);
        this.getProduct = this.getProduct.bind(this);
        this.checkReaction = this.checkReaction.bind(this);
    }

    componentDidMount() {
        var state = this.props.parent.state;
        state.viewProduct = this;
        this.props.parent.setState(state);
    }

    reloadAjaxRequest(option) {
        var state = this.state;

        switch(option){
            case 1:{

                if (state.ajax.retrieveProfileData.attempts < 10) {
                    state.ajax.retrieveProfileData.attempts += 1;
                    this.setState(state);
                    this.retrieveProfileData();
                }
                else {
                    state.errorPopup.displayError("Access to server failed. Try again Later! ");
                    state.ajax.retrieveProfileData.attempts = 0;
                    this.setState(state);
                }
                break;
            }
            case 2: {

                if (state.ajax.getProduct.attempts < 10) {
                    state.ajax.getProduct.attempts += 1;
                    this.setState(state);
                    this.getProduct();
                }
                else {
                    state.errorPopup.displayError("Access to server failed. Try again Later! ");
                    state.ajax.getProduct.attempts = 0;
                    this.setState(state);
                }
                break;
            }
        }

    }

    setCoverPhoto(){
        var state = this.state;
        var product = state.product.data.post;
        state.coverPhotoUrl = product.image != undefined ? webUrl + 'repo/' + product.image.name + "." + product.image.type : defaultProductCoverPic;
        this.setState(state);
    }

    getProduct() {
        var component = this;
        var state = this.state;

        if(state.commentingSystem.state != undefined ){
            state.commentingSystem.clearComments();
        }

        axios({
            url: webUrl + "getProduct/" + state.product.id,
            method:"GET"
        }).then((response) => {
            
            if(response.status == 200){
                var data = response.data;
                state.product.data = data.content;
                state.likes = data.content.likes == undefined ? 0 : data.content.likes.length;
                component.setState(state);

                if (state.commentingSystem.state != undefined) {
                    state.commentingSystem.getComments();
                }

                setTimeout(() => {
                    component.setCoverPhoto();
                }, 1000);
            }

        }).catch((response)=>{
            if(response.status != 200){
                component.reloadAjaxRequest(3);
            }
        })

    }

    reactToProduct(reaction = 1) {
        var component = this;
        var state = component.state;
        var url = webUrl + "productReaction/" + this.state.product.data.post.id + "/" ;
        url+= state.reaction == reaction ? 0 : reaction;

        axios({
            url:url,
            method:"GET"
        }).then((response)=>{
            
            if (response.status == 200){
                var ind = state.product.stats.findIndex((item) => {
                    return item.user == state.userId;
                })

                if (ind < 0) {
                    state.product.stats[ind].reaction = state.reaction == reaction ? 0 : reaction;
                }

                switch (state.reaction) {
                    case 0: {
                        switch (reaction) {
                            case 1: {
                                state.stats.likes++;
                                break;
                            }
                            case 2: {
                                state.stats.dislikes++;
                                break;
                            }
                        }
                        break;
                    }
                    case 1: {
                        switch (reaction) {
                            case 2: {
                                state.stats.likes--;
                                state.stats.dislikes++;
                                break;
                            }
                        }
                        break;
                    }
                    case 2: {
                        switch (reaction) {
                            case 1: {
                                state.stats.dislikes--;
                                state.stats.likes++;
                                break;
                            }
                        }
                        break;
                    }
                }

                component.setState(state);
                component.checkReaction();
            }

        }).catch((response) => {
            switch(response.status){
                case 404:{
                    component.state.errorPopup.displayError('Product not found. Please try again later!');
                    break;
                }
                default:{
                    component.state.errorPopup.displayError('Error accessing server. Please try again later!');
                    break;
                }
            }

        })
    }


    checkReaction() {
        var product = this.state.product.data.post;
        var state = this.state;

        var reaction = product.stats.find((item) => {
            return item.user == state.userId;
        })

        state.reaction = reaction == undefined ? 0 : reaction.reaction;

        state.buttons[0].state.status = state.reaction == 2 ? 5 : 0;
        state.buttons[0].state.label = state.reaction == 2 ? "Disliked" : "Dislike";
        state.buttons[1].state.status = state.reaction == 1 ? 6 : 0;
        state.buttons[1].state.label = state.reaction == 1 ? "Liked" : "Like";

        this.setState(state);
    }

    render() {
        var product = this.state.product.data.post;
        if (product == undefined) { return <div></div>; }

        var coverImage = {
            backgroundImage: "url('" + this.state.coverPhotoUrl + "')",
            backgroundSize:'cover',
            backgroundPosition:'center'
        }

        var parent = this.props.parent;

        var time = moment(this.state.product.data.log.created_at,"YYYY-MM-DD HH:mm:ss").utc(3).local();
        var ctime = moment.duration(time.diff(moment()),'milliseconds').humanize();

        return (
            <div className="vP">
                <ErrorPopup parent={this} />

                <div className="pageTop">
                    <div className="pageTop__background" style={coverImage}></div>
                    <div className="pageTop__foreground"></div>
                </div>

                <div className="section">

                    <StickyBox >
                        <div className="section__1"></div>
                    </StickyBox>
                    
                    <StickyBox >
                        
                        <div className="section__2">
                            <div className="navigation">
                                <div className="navigation__home">
                                    <ButtonWithIcon
                                        parent={this}
                                        status={0}
                                        config={{
                                            class: "btnIcon_1",
                                            action: () => { 
                                                parent.setView(1);
                                            },
                                            label: "Back",
                                            icon: "back"
                                        }}
                                    />
                                </div>



                                <div className="navigation__stat">
                                    <div className="navigation__stat__view">
                                        <div className="navigation__stat__icon">
                                            <div className="iconBtn--normal">
                                                <svg className="icon">
                                                    <use xlinkHref="#view" />
                                                </svg>
                                            </div>
                                        </div>
                                        <div className="navigation__stat__value f_h2 f_text-bold">{product.stat.views}</div>
                                    </div>

                                    <div className="navigation__stat__likes">
                                        <div className="navigation__stat__icon">
                                            <div className="iconBtn--normal">
                                                <svg className="icon">
                                                    <use xlinkHref="#like" />
                                                </svg>
                                            </div>
                                        </div>
                                        <div className="navigation__stat__value f_h2 f_text-bold">{this.state.likes}</div>
                                    </div>

                                    <div className="navigation__stat__com">
                                        <div className="navigation__stat__icon">
                                            <div className="iconBtn--normal">
                                                <svg className="icon">
                                                    <use xlinkHref="#communication" />
                                                </svg>
                                            </div>
                                        </div>
                                        <div className="navigation__stat__value f_h2 f_text-bold">{product.stat.comments}</div>
                                    </div>

                                </div>

                                <div className="navigation__buttons">
                                    <div className="navigation__buttons__button">
                                        <ButtonWithIcon
                                            parent={this}
                                            status={ this.state.reaction == 2 ? 5 : 0}
                                            config={{
                                                class: "btnIcon_2",
                                                action: () => { this.reactToProduct(2)},
                                                label: this.state.reaction == 2 ? "Disliked" : "Dislike",
                                                icon: "dislike"
                                            }}
                                        />
                                    </div>
                                    <div className="navigation__buttons__button">
                                        <ButtonWithIcon 
                                            parent={this}
                                            status={this.state.reaction == 1 ? 6 : 0}
                                            config={{
                                                class:"btnIcon_2",
                                                action: () => { this.reactToProduct(1) },
                                                label: this.state.reaction == 1 ? "Liked" : "Like",
                                                icon:"like"
                                            }}
                                        />
                                    </div>
                                </div>

                            </div>

                            <div className="product">
                                <div className="product__content">
                                    <div className="product__primary">

                                        <div className="product__title f_title f_text-capitalize">{product.title}</div>
                                        <div className="product__time f_normal">{ctime + " ago"}</div>

                                    </div>
                                    <div className="product__tags">
                                        {
                                            product.tags.map((item, i) => {
                                                return (<div className="product__tag f_normal" key={i}>{item.name}</div>);
                                            })
                                        }
                                    </div>

                                    <div className="product__text">
                                        <div className="ck--1" dangerouslySetInnerHTML={{ __html: product.body }}></div>
                                    </div>

                                </div>

                            <div className="product__commentSection">
                                <CommentingSystem commentingOn={1} product={this.state.product.data} parent={this}/>
                            </div> 

                            </div>

                        </div>

                    </StickyBox>

                    

                    <StickyBox >
                        <div className="section__3"></div>
                    </StickyBox>
                    
                </div>  
            </div>
        );
    }
}


export default ViewProduct;