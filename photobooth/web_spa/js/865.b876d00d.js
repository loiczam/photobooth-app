"use strict";(globalThis["webpackChunkqPhotobooth"]=globalThis["webpackChunkqPhotobooth"]||[]).push([[865],{6446:(e,t,i)=>{i.d(t,{Z:()=>L});var r=i(9835),n=i(6970);const l={key:4,class:"q-mr-sm"},a={class:"q-mr-sm"},o={class:"absolute-bottom-left text-subtitle2"},s=["src"],d={class:"q-gutter-sm"};function c(e,t,i,c,g,m){const u=(0,r.up)("q-btn"),p=(0,r.up)("q-space"),h=(0,r.up)("q-icon"),y=(0,r.up)("q-toolbar"),S=(0,r.up)("q-linear-progress"),w=(0,r.up)("q-header"),f=(0,r.up)("q-img"),v=(0,r.up)("q-drawer"),I=(0,r.up)("q-carousel-slide"),q=(0,r.up)("q-carousel"),b=(0,r.up)("vue-qrcode"),k=(0,r.up)("q-page-sticky"),_=(0,r.up)("q-page-container"),R=(0,r.up)("q-layout"),x=(0,r.Q2)("touch-swipe");return(0,r.wg)(),(0,r.j4)(R,{view:"hhh Lpr ffr",onClick:m.abortTimer},{default:(0,r.w5)((()=>[(0,r.Wm)(w,{elevated:"",class:"bg-primary text-white"},{default:(0,r.w5)((()=>[(0,r.Wm)(y,null,{default:(0,r.w5)((()=>[(0,r.Wm)(u,{dense:"",flat:"",icon:"close",onClick:t[0]||(t[0]=t=>e.$emit("closeEvent"))}),(0,r.Wm)(p),c.uiSettingsStore.uiSettings.gallery_show_delete?((0,r.wg)(),(0,r.j4)(u,{key:0,flat:"",class:"q-mr-sm",icon:"delete",label:"Delete",onClick:t[1]||(t[1]=t=>{m.deleteItem(c.currentSlideId),e.$emit("closeEvent")})})):(0,r.kq)("",!0),c.uiSettingsStore.uiSettings.gallery_show_download?((0,r.wg)(),(0,r.j4)(u,{key:1,flat:"",class:"q-mr-sm",icon:"download",label:"Download",onClick:t[2]||(t[2]=e=>{c.openURL(i.itemRepository[c.currentSlideIndex]["full"])})})):(0,r.kq)("",!0),c.uiSettingsStore.uiSettings.gallery_show_print?((0,r.wg)(),(0,r.j4)(u,{key:2,flat:"",class:"q-mr-sm",icon:"print",label:"Print",onClick:t[3]||(t[3]=e=>m.printItem(c.currentSlideId))})):(0,r.kq)("",!0),c.uiSettingsStore.uiSettings.gallery_show_filter&&c.uiSettingsStore.uiSettings.gallery_filter_userselectable.length>0?((0,r.wg)(),(0,r.j4)(u,{key:3,flat:"",class:"q-mr-sm",icon:"filter",label:"Filter",onClick:c.toggleRightDrawer},null,8,["onClick"])):(0,r.kq)("",!0),(0,r.Wm)(p),i.itemRepository.length>1?((0,r.wg)(),(0,r.iD)("div",l,[(0,r.Wm)(h,{name:"tag"}),(0,r._)("span",null,(0,n.zw)(c.currentSlideIndex+1)+" of "+(0,n.zw)(i.itemRepository.length)+" total",1)])):(0,r.kq)("",!0),(0,r.Wm)(p),(0,r._)("div",a,[(0,r.Wm)(h,{name:"image"}),(0,r.Uk)(" "+(0,n.zw)(i.itemRepository[c.currentSlideIndex]["caption"]),1)])])),_:1}),g.displayLinearProgressBar&&g.remainingSeconds>0?((0,r.wg)(),(0,r.j4)(S,{key:0,class:"absolute",value:g.remainingSecondsNormalized,"animation-speed":"200",color:"grey"},null,8,["value"])):(0,r.kq)("",!0),c.displayLoadingSpinner?((0,r.wg)(),(0,r.j4)(S,{key:1,class:"absolute",indeterminate:"","animation-speed":"2100",color:"primary"})):(0,r.kq)("",!0)])),_:1}),c.uiSettingsStore.uiSettings.gallery_show_filter?((0,r.wg)(),(0,r.j4)(v,{key:0,modelValue:c.rightDrawerOpen,"onUpdate:modelValue":t[4]||(t[4]=e=>c.rightDrawerOpen=e),side:"right",elevated:"",overlay:""},{default:(0,r.w5)((()=>[((0,r.wg)(!0),(0,r.iD)(r.HY,null,(0,r.Ko)(c.uiSettingsStore.uiSettings.gallery_filter_userselectable,(e=>((0,r.wg)(),(0,r.j4)(f,{src:`/mediaprocessing/preview/${c.currentSlideId}/${e}`,key:e,onClick:t=>m.applyFilter(c.currentSlideId,e)},{default:(0,r.w5)((()=>[(0,r._)("div",o,(0,n.zw)(e),1)])),_:2},1032,["src","onClick"])))),128))])),_:1},8,["modelValue"])):(0,r.kq)("",!0),(0,r.Wm)(_,{class:"q-pa-none galleryimagedetail full-height"},{default:(0,r.w5)((()=>[(0,r.wy)(((0,r.wg)(),(0,r.j4)(q,{style:{width:"100%",height:"100%"},"control-type":"flat","control-color":"primary",swipeable:"",animated:"",modelValue:c.currentSlideId,"onUpdate:modelValue":t[5]||(t[5]=e=>c.currentSlideId=e),autoplay:c.autoplay,draggable:"false",arrows:"","transition-prev":"slide-right","transition-next":"slide-left",onTransition:t[6]||(t[6]=(e,t)=>{c.currentSlideIndex=i.itemRepository.findIndex((t=>t.id===e)),m.abortTimer()})},{default:(0,r.w5)((()=>[((0,r.wg)(!0),(0,r.iD)(r.HY,null,(0,r.Ko)(m.slicedImages,(e=>((0,r.wg)(),(0,r.j4)(I,{key:e.id,name:e.id,class:"column no-wrap flex-center full-height"},{default:(0,r.w5)((()=>[(0,r._)("img",{draggable:!1,class:"rounded-borders full-height",style:{"object-fit":"contain","max-width":"100%","max-height":"100%"},src:e.preview},null,8,s)])),_:2},1032,["name"])))),128))])),_:1},8,["modelValue","autoplay"])),[[x,c.handleSwipeDown,void 0,{mouse:!0,down:!0}]]),(0,r.Wm)(k,{position:"top-right",offset:[30,30]},{default:(0,r.w5)((()=>[(0,r._)("div",d,[(0,r.Wm)(b,{type:"image/png",tag:"svg",margin:2,width:200,"error-correction-level":"low",color:{dark:"#111111",light:"#EEEEEE"},value:m.getImageQrData()},null,8,["value"])])])),_:1})])),_:1})])),_:1},8,["onClick"])}i(9665);var g=i(528),m=i(499),u=i(6694),p=i(3752),h=i(9302);const y={props:{indexSelected:{type:Number,required:!0},itemRepository:{type:Array,required:!0},startTimerOnOpen:{type:Boolean,required:!1,default:!1}},computed:{slicedImages(){this.itemRepository.length;var e=Math.max(0,this.currentSlideIndex-2),t=Math.max(0,this.currentSlideIndex+3);return this.itemRepository.slice(e,t)}},beforeCreate(){console.log(this.indexSelected),this.currentSlideIndex=this.indexSelected,this.currentSlideId=this.itemRepository[this.indexSelected].id},data(){return{intervalTimerId:null,remainingSeconds:0,remainingSecondsNormalized:0,displayLinearProgressBar:!0}},setup(){const e=(0,u.R)(),t=(0,m.iH)(!1);(0,h.Z)();return{uiSettingsStore:e,openURL:p.Z,fabRight:(0,m.iH)(!1),currentSlideId:(0,m.iH)(""),currentSlideIndex:(0,m.iH)(0),autoplay:(0,m.iH)(!1),showFilterDialog:(0,m.iH)(!1),displayLoadingSpinner:(0,m.iH)(!1),rightDrawerOpen:t,toggleRightDrawer(){t.value=!t.value},handleSwipeDown({evt:e}){console.log("TODO: add method to close dialog programmatically")}}},components:{VueQrcode:g.ZP},mounted(){this.startTimerOnOpen&&this.startTimer()},beforeUnmount(){clearInterval(this.intervalTimerId)},methods:{async reloadImg(e){await fetch(e,{cache:"reload",mode:"no-cors"});const t=(new Date).getTime();document.body.querySelectorAll(`img[src*='${e}']`).forEach((i=>{i.src=e+"#"+t}))},applyFilter(e,t){this.displayLoadingSpinner=!0,this.$api.get(`/mediaprocessing/applyfilter/${e}/${t}`).then((t=>{const i=this.itemRepository.findIndex((t=>t.id===e));this.reloadImg(this.itemRepository[i].full),this.reloadImg(this.itemRepository[i].preview),this.reloadImg(this.itemRepository[i].thumbnail),this.displayLoadingSpinner=!1})).catch((e=>{console.log(e),this.displayLoadingSpinner=!1}))},deleteItem(e){this.$api.get("/mediacollection/delete",{params:{image_id:e}}).then((e=>{console.log(e),this.itemRepository.splice(this.currentSlideIndex,1)})).catch((e=>console.log(e)))},printItem(e){this.$api.get(`/print/item/${e}`).then((e=>{console.log(e),this.$q.notify({message:"Started printing...",type:"positive",spinner:!0})})).catch((e=>{e.response?(console.log(e.response),425==e.response.status?this.$q.notify({message:e.response.data["detail"],caption:"Print Service",type:"info"}):this.$q.notify({message:e.response.data["detail"],caption:"Print Service",type:"negative"})):e.request?console.error(e.request):console.error("Error",e.message)}))},getImageDetail(e,t="thumbnail"){return this.itemRepository[e][t]},getImageQrData(){return this.itemRepository[this.currentSlideIndex]["share_url"]},abortTimer(){clearInterval(this.intervalTimerId),this.remainingSeconds=0,this.remainingSecondsNormalized=0},startTimer(){var e=this.uiSettingsStore.uiSettings["AUTOCLOSE_NEW_ITEM_ARRIVED"];console.log(`starting newitemarrived timer, duration=${e}`),this.remainingSeconds=e,this.intervalTimerId=setInterval((()=>{this.remainingSecondsNormalized=this.remainingSeconds/e,this.remainingSeconds-=.05,this.remainingSeconds<=0&&(clearInterval(this.intervalTimerId),this.$router.push({path:"/"}))}),50)}}};var S=i(1639),w=i(7605),f=i(6602),v=i(1663),I=i(8879),q=i(136),b=i(2857),k=i(8289),_=i(906),R=i(335),x=i(2133),D=i(7052),T=i(1694),Z=i(627),C=i(4871),Q=i(9984),$=i.n(Q);const E=(0,S.Z)(y,[["render",c],["__scopeId","data-v-096d82e9"]]),L=E;$()(y,"components",{QLayout:w.Z,QHeader:f.Z,QToolbar:v.Z,QBtn:I.Z,QSpace:q.Z,QIcon:b.Z,QLinearProgress:k.Z,QDrawer:_.Z,QImg:R.Z,QPageContainer:x.Z,QCarousel:D.Z,QCarouselSlide:T.Z,QPageSticky:Z.Z}),$()(y,"directives",{TouchSwipe:C.Z})},865:(e,t,i)=>{i.r(t),i.d(t,{default:()=>p});var r=i(9835);function n(e,t,i,n,l,a){const o=(0,r.up)("gallery-image-detail"),s=(0,r.up)("q-page");return(0,r.wg)(),(0,r.j4)(s,{class:"q-pa-none fullscreen"},{default:(0,r.w5)((()=>[(0,r.Wm)(o,{onCloseEvent:t[0]||(t[0]=t=>e.$router.go(-1)),itemRepository:[this.store.gallery.newArrivalItem],indexSelected:0,startTimerOnOpen:!0,class:"full-height"},null,8,["itemRepository"])])),_:1})}var l=i(7575),a=i(6694),o=i(6446);const s={components:{GalleryImageDetail:o.Z},data(){return{intervalTimerId:null,remainingSeconds:0,remainingSecondsNormalized:0,displayLinearProgressBar:!0,showImageDetail:!0}},setup(){const e=(0,l.h)(),t=(0,a.R)();return{store:e,uiSettingsStore:t,GalleryImageDetail:o.Z}},mounted(){},beforeUnmount(){},methods:{}};var d=i(1639),c=i(9885),g=i(9984),m=i.n(g);const u=(0,d.Z)(s,[["render",n]]),p=u;m()(s,"components",{QPage:c.Z})}}]);