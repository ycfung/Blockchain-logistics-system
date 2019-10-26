// pages/history/history.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    takenList: [],
    inputVal: "",
    oneRes: null,
    ans:"",
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.loadData();
  },
  
  
  loadData: function () {
    var that = this;
    wx.showLoading()
    wx.request({
      url: 'http://localhost:8888/MyDemo/History',
      method: 'GET',
      header: { 'content-type': 'application/json' },
      success: function (res) {
        that.setData({
          takenList: res.data.takenList
        })
        console.log(res.data);
        wx.showToast({ title: '数据加载完成' })
      },
      fail: function (res) {
        wx.showToast({ title: '数据加载失败' })
      }
    })
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

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
  

 showInput: function () {
    this.setData({
      inputShowed: true
    });
  },
  hideInput: function () {
    this.setData({
      inputVal: "",
      inputShowed: false
    });
  },
  clearInput: function () {
    this.setData({
      inputVal: ""
    });
  },
  inputTyping: function (e) {
    this.setData({
      inputVal: e.detail.value
    });
  },
  search: function () {
    var flag = false;
    var list = this.data.takenList;
    console.log(list)
    for (var i=0; i<list.length; i++){
      if (list[i].pNumber == this.data.inputVal){
        this.setData({
          oneRes: list[i],
        });
        flag = true;
        break;
      }
    }
    console.log(this.data.oneRes);
    if(!flag){
      this.setData({
        ans : "无结果"
      });
    }
  }
})