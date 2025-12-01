import streamlit as st
import boto3

# 初始化页面配置
st.set_page_config(page_title="运维告警Demo", page_icon="🔊")

connect_client = boto3.client("connect")

# 设置页面标题
st.title("运维告警Demo")

# 发起一个外呼语音电话
def start_outbound_voice_call(
    phone_number,
    alert_content,
    connect_instance_id,
    contact_flow_id,
    source_phone_number=None
):
    try:
        # 初始化 Amazon Connect 客户端
        connect_client = boto3.client('connect')
        
        # 准备默认属性
        alert_msg = f"<speak><break time='1s'/>{alert_content}</speak>"
        attributes = {
            'alertMessage': alert_msg
        }
        
        # 准备 API 调用参数
        params = {
            'DestinationPhoneNumber': phone_number,
            'ContactFlowId': contact_flow_id,
            'InstanceId': connect_instance_id,
            'Attributes': attributes
        }
        
        # 添加可选参数（如果提供）
        if source_phone_number:
            params['SourcePhoneNumber'] = source_phone_number
        
        # 发起外呼电话
        response = connect_client.start_outbound_voice_contact(**params)
        
        print(f"成功发起外呼电话到 {phone_number}，ContactId: {response['ContactId']}")
        return response
        
    except Exception as e:
        print(f"发生未预期的错误: {str(e)}")
        raise

# 创建表单
with st.form("alert_form"):
    # 手机号码输入
    phone_number = st.text_input("请输入手机号码", 
                                placeholder="+18007282584",
                                value="+18007282584",
                                max_chars=12)
    
    # 告警内容输入
    alert_content = st.text_area("请输入告警内容",
                                value="紧急通知：生产环境数据库CPU使用率已达到95%，请立即处理。",
                                placeholder="请输入告警信息...",
                                height=100)
    
    # Connect Instance ID 输入
    connect_instance_id = st.text_input("Connect Instance ID",
                                       placeholder="b7e4b4ed-1bdf-4b14-b624-d9328f08725a",
                                       value="b7e4b4ed-1bdf-4b14-b624-d9328f08725a")
    
    # Contact Flow ID 输入
    contact_flow_id = st.text_input("Contact Flow ID",
                                   placeholder="5b46da68-f82f-4dd8-8500-d906c541293e",
                                   value="5b46da68-f82f-4dd8-8500-d906c541293e")
    
    st.write("中文flow - 5b46da68-f82f-4dd8-8500-d906c541293e")
    st.write("English flow - 0d8089db-c817-4006-a1d1-4a71fc7e9b6b")
    
    # 生成告警按钮
    if st.form_submit_button("发送告警"):
        if not phone_number or len(phone_number) != 12:
            st.error("请输入有效的手机号码")
        elif not alert_content:
            st.error("请输入告警内容")
        elif not connect_instance_id:
            st.error("请输入Connect Instance ID")
        elif not contact_flow_id:
            st.error("请输入Contact Flow ID")
        else:
            # 发送告警
            st.toast(f"正在通过语音将告警发送至 {phone_number}")
            
            # 发起语音通话
            try:
                start_outbound_voice_call(
                    phone_number, 
                    alert_content,
                    connect_instance_id,
                    contact_flow_id,
                    '+13072633584'
                )
                st.success(f"告警已成功发送至 {phone_number}")
            except Exception as e:
                st.error(f"发送失败: {str(e)}")