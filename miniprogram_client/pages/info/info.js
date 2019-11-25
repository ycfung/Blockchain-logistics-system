// pages/info/info.js
const app=getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {

    credit: 100,
    articles: {
      name:"",
      tele:"",
      addr:"",
      number:""
    }
    },


  

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    // this.loadData(true);
    this.setData({
      articles: wx.getStorageSync('case001')
    })
    //console.log(this.articles);

  },
  goToIndexPage: function(){
    wx.navigateBack({
      delta: 1
    });
  },
  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {
  
  },
  getkey:function(){
  
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
   // this.name1 = app.name; 
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  },
  //e.detail.value.name 其中的name是指组件中的名字属性
  formSubmit1:function(e){

  this.setData({
    articles:e.detail.value
  })
    wx.setStorageSync('case001', this.data.articles);
    //在这里可以判断是否已经生成过私钥，若没生成过，那么再在这里生成私钥
    if (wx.getStorageSync('case001')=='')
    {
      //生成私钥并存储
    }
    var that = this;
    var formData = e.detail.value;
    if (e.detail.value.name == '' || e.detail.value.tele == '' || e.detail.value.number == '' || e.detail.value.addr == ''||app.key == '') {
      wx.showToast({
        title: '请填写完整···',
      })
    } else {
      wx.request({
        url: 'http://101.132.96.109:8000/',//这里的接口请填实际接口     
        data: {
          notify: 5,
          number: app.number,
          formData

        },

        header: {
          'Content-Type': 'application/json'
        },
        //这里设置成功的返回信息
        success: function (res) {
          console.log(res.data)
          that.setData({
            form_info: ''
          })
        }
      })
    }
   
  },
 
  loadData: function (tail, callback) {

  },
})