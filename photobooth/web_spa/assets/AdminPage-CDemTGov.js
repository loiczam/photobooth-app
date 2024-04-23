import{_ as T,f as b,n as A,p as s,q as e,H as $,j as S,F as B,r as u,m as g,B as r,D as m,W as _,X as d,a1 as p,a2 as f,a3 as L,z as n,Q as t,a4 as i}from"./index-7q0rWrNn.js";import{Q as w}from"./QPage-DxaNNaMf.js";import{Q as I}from"./QSelect-PKObr3yo.js";import{u as V}from"./vue-i18n.runtime-CORBGzXE.js";import"./rtl-CF_aSVsN.js";import"./QItemLabel-g6bGkJMN.js";import"./selection-Dhu-KKnd.js";import"./format-CJebrXOQ.js";const y={setup(){const{locale:l,availableLocales:a}=V({useScope:"global"}),v=new Intl.DisplayNames(["en"],{type:"language",languageDisplay:"standard"}),c=a.map(function(C){return{value:C,label:v.of(C)}});return{locale:l,localeOptions:c}},methods:{storeLocale(l){localStorage.setItem("locale",l),console.log("Stored locale: ",l)}}};function R(l,a,v,c,C,N){return b(),A(I,{modelValue:c.locale,"onUpdate:modelValue":[a[0]||(a[0]=E=>c.locale=E),a[1]||(a[1]=E=>N.storeLocale(E))],options:c.localeOptions,label:"Language","emit-value":"","map-options":""},{prepend:s(()=>[e($,{name:"language"})]),_:1},8,["modelValue","options"])}const q=T(y,[["render",R],["__file","LanguageSwitcher.vue"]]),O=S({name:"MainLayout",components:{LanguageSwitcher:q},setup(){return{remoteProcedureCall:B,confirm_reboot:u(!1),confirm_shutdown:u(!1),confirm_restart_service:u(!1),confirm_reload_service:u(!1),confirm_install_service:u(!1),confirm_uninstall_service:u(!1),confirm_delete_all:u(!1)}}}),M={class:"text-h5"},D={class:"row"},k={class:"q-ma-sm"},U={class:"text-no-wrap"},P={class:"q-ml-sm"},Q={class:"q-ml-sm"},h={class:"q-ml-sm"},F={class:"q-ml-sm"},G={class:"q-ml-sm"},H={class:"q-ml-sm"},W={class:"text-h5"},j={class:"row"},z={class:"q-ma-sm"},X={class:"text-no-wrap"},Y={class:"q-ml-sm"},J={class:"text-h5"},K={class:"row"};function Z(l,a,v,c,C,N){const E=g("language-switcher");return b(),A(w,{padding:""},{default:s(()=>[e(d,{class:"q-pa-md"},{default:s(()=>[r("div",M,m(l.$t("TITLE_SERVER_CONTROL")),1),r("div",D,[r("div",k,[r("div",U,[e(_,{modelValue:l.confirm_reboot,"onUpdate:modelValue":a[1]||(a[1]=o=>l.confirm_reboot=o)},{default:s(()=>[e(d,{class:"q-pa-sm",style:{"min-width":"350px"}},{default:s(()=>[e(p,{class:"row items-center"},{default:s(()=>[e(f,{icon:"restart_alt",color:"primary","text-color":"white"}),r("span",P,m(l.$t("MSG_CONFIRM_REBOOT")),1)]),_:1}),e(L,{align:"right"},{default:s(()=>[n(e(t,{flat:"",label:l.$t("BTN_LABEL_CANCEL"),color:"primary"},null,8,["label"]),[[i]]),n(e(t,{label:l.$t("BTN_LABEL_REBOOT"),color:"primary",onClick:a[0]||(a[0]=o=>l.remoteProcedureCall("/api/system/server/reboot"))},null,8,["label"]),[[i]])]),_:1})]),_:1})]),_:1},8,["modelValue"]),e(_,{modelValue:l.confirm_shutdown,"onUpdate:modelValue":a[3]||(a[3]=o=>l.confirm_shutdown=o)},{default:s(()=>[e(d,{class:"q-pa-sm",style:{"min-width":"350px"}},{default:s(()=>[e(p,{class:"row items-center"},{default:s(()=>[e(f,{icon:"power_settings_new",color:"primary","text-color":"white"}),r("span",Q,m(l.$t("MSG_CONFIRM_SHUTDOWN")),1)]),_:1}),e(L,{align:"right"},{default:s(()=>[n(e(t,{flat:"",label:l.$t("BTN_LABEL_CANCEL")},null,8,["label"]),[[i]]),n(e(t,{label:l.$t("BTN_LABEL_SHUTDOWN"),color:"primary",onClick:a[2]||(a[2]=o=>l.remoteProcedureCall("/api/system/server/shutdown"))},null,8,["label"]),[[i]])]),_:1})]),_:1})]),_:1},8,["modelValue"]),e(_,{modelValue:l.confirm_restart_service,"onUpdate:modelValue":a[5]||(a[5]=o=>l.confirm_restart_service=o)},{default:s(()=>[e(d,{class:"q-pa-sm",style:{"min-width":"350px"}},{default:s(()=>[e(p,{class:"row items-center"},{default:s(()=>[e(f,{icon:"restart_alt",color:"primary","text-color":"white"}),r("span",h,m(l.$t("MSG_CONFIRM_RESTART_SERVICE")),1)]),_:1}),e(L,{align:"right"},{default:s(()=>[n(e(t,{flat:"",label:l.$t("BTN_LABEL_CANCEL")},null,8,["label"]),[[i]]),n(e(t,{label:l.$t("BTN_LABEL_RESTART_SERVICE"),color:"primary",onClick:a[4]||(a[4]=o=>l.remoteProcedureCall("/api/system/service/restart"))},null,8,["label"]),[[i]])]),_:1})]),_:1})]),_:1},8,["modelValue"]),e(_,{modelValue:l.confirm_reload_service,"onUpdate:modelValue":a[7]||(a[7]=o=>l.confirm_reload_service=o)},{default:s(()=>[e(d,{class:"q-pa-sm",style:{"min-width":"350px"}},{default:s(()=>[e(p,{class:"row items-center"},{default:s(()=>[e(f,{icon:"restart_alt",color:"primary","text-color":"white"}),r("span",F,m(l.$t("MSG_CONFIRM_RELOAD_SERVICE")),1)]),_:1}),e(L,{align:"right"},{default:s(()=>[n(e(t,{flat:"",label:l.$t("BTN_LABEL_CANCEL")},null,8,["label"]),[[i]]),n(e(t,{label:l.$t("BTN_LABEL_RELOAD_SERVICE"),color:"primary",onClick:a[6]||(a[6]=o=>l.remoteProcedureCall("/api/system/service/reload"))},null,8,["label"]),[[i]])]),_:1})]),_:1})]),_:1},8,["modelValue"]),e(_,{modelValue:l.confirm_install_service,"onUpdate:modelValue":a[9]||(a[9]=o=>l.confirm_install_service=o)},{default:s(()=>[e(d,{class:"q-pa-sm",style:{"min-width":"350px"}},{default:s(()=>[e(p,{class:"row items-center"},{default:s(()=>[e(f,{icon:"add_circle",color:"primary","text-color":"white"}),r("span",G,m(l.$t("MSG_CONFIRM_INSTALL_SERVICE")),1)]),_:1}),e(L,{align:"right"},{default:s(()=>[n(e(t,{flat:"",label:l.$t("BTN_LABEL_CANCEL")},null,8,["label"]),[[i]]),n(e(t,{label:l.$t("BTN_LABEL_INSTALL_SERVICE"),color:"primary",onClick:a[8]||(a[8]=o=>l.remoteProcedureCall("/api/system/service/install"))},null,8,["label"]),[[i]])]),_:1})]),_:1})]),_:1},8,["modelValue"]),e(_,{modelValue:l.confirm_uninstall_service,"onUpdate:modelValue":a[11]||(a[11]=o=>l.confirm_uninstall_service=o)},{default:s(()=>[e(d,{class:"q-pa-sm",style:{"min-width":"350px"}},{default:s(()=>[e(p,{class:"row items-center"},{default:s(()=>[e(f,{icon:"cancel",color:"primary","text-color":"white"}),r("span",H,m(l.$t("MSG_CONFIRM_UNINSTALL_SERVICE")),1)]),_:1}),e(L,{align:"right"},{default:s(()=>[n(e(t,{flat:"",label:l.$t("BTN_LABEL_CANCEL")},null,8,["label"]),[[i]]),n(e(t,{label:l.$t("BTN_LABEL_UNINSTALL_SERVICE"),color:"primary",onClick:a[10]||(a[10]=o=>l.remoteProcedureCall("/api/system/service/uninstall"))},null,8,["label"]),[[i]])]),_:1})]),_:1})]),_:1},8,["modelValue"]),e(t,{class:"q-mr-sm",label:l.$t("BTN_LABEL_REBOOT_HOST"),onClick:a[12]||(a[12]=o=>l.confirm_reboot=!0)},null,8,["label"]),e(t,{class:"q-mr-sm",label:l.$t("BTN_LABEL_SHUTDOWN_HOST"),onClick:a[13]||(a[13]=o=>l.confirm_shutdown=!0)},null,8,["label"]),e(t,{class:"q-mr-sm",label:l.$t("BTN_LABEL_RESTART_SERVICE"),onClick:a[14]||(a[14]=o=>l.confirm_restart_service=!0)},null,8,["label"]),e(t,{class:"q-mr-sm",label:l.$t("BTN_LABEL_INSTALL_SERVICE"),onClick:a[15]||(a[15]=o=>l.confirm_install_service=!0)},null,8,["label"]),e(t,{class:"q-mr-sm",label:l.$t("BTN_LABEL_UNINSTALL_SERVICE"),onClick:a[16]||(a[16]=o=>l.confirm_uninstall_service=!0)},null,8,["label"])])])])]),_:1}),e(d,{class:"q-pa-md q-mt-md"},{default:s(()=>[r("div",W,m(l.$t("TITLE_MAINTAIN_GALLERY")),1),r("div",j,[r("div",z,[r("div",X,[e(_,{modelValue:l.confirm_delete_all,"onUpdate:modelValue":a[18]||(a[18]=o=>l.confirm_delete_all=o)},{default:s(()=>[e(d,{class:"q-pa-sm"},{default:s(()=>[e(p,{class:"row items-center"},{default:s(()=>[e(f,{icon:"delete",color:"primary","text-color":"white"}),r("span",Y,m(l.$t("MSG_CONFIRM_DELETE_ALL_MEDIA_FILES")),1)]),_:1}),e(L,{align:"right"},{default:s(()=>[n(e(t,{flat:"",label:"Cancel",color:"primary"},null,512),[[i]]),n(e(t,{label:"Delete all",color:"primary",onClick:a[17]||(a[17]=o=>l.remoteProcedureCall("/api/mediacollection/delete_all"))},null,512),[[i]])]),_:1})]),_:1})]),_:1},8,["modelValue"]),e(t,{class:"q-mr-sm",label:l.$t("BTN_LABEL_DELETE_ALL_MEDIA_FILES"),onClick:a[19]||(a[19]=o=>l.confirm_delete_all=!0)},null,8,["label"])])])])]),_:1}),e(d,{class:"q-pa-md q-mt-md"},{default:s(()=>[r("div",J,m(l.$t("TITLE_LOCAL_UI_SETTINGS")),1),r("div",K,[e(E)])]),_:1})]),_:1})}const nl=T(O,[["render",Z],["__file","AdminPage.vue"]]);export{nl as default};
