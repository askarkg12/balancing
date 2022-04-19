#include <micro_ros_arduino.h>
#include <rcl/rcl.h>
#include <rcl/error_handling.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>

#include <sensor_msgs/msg/imu.h>
#include <std_msgs/msg/int64.h>
//#include <geometry_msgs/msg/Quaternion.h>

#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

Adafruit_MPU6050 mpu;

rcl_subscription_t subscriber;
rcl_publisher_t publisher;
rclc_executor_t executor;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_node_t node;
rcl_timer_t timer;

rcl_timer_t motor_timer;
unsigned long last_cmd_vel_time;
const unsigned int motor_timeout = 1000;
const unsigned int motor_period = 100;

elapsedMillis millisPassed;

sensor_msgs__msg__Imu imu_msg;
std_msgs__msg__Int64 period_msg;
sensors_event_t a, g, temp;
//geometry_msgs__msg__Quaternion orientation;

#define LED_PIN 13

#define RCCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){error_loop();}}
#define RCSOFTCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){}}

void error_loop(){
  while(1){
    digitalWrite(LED_PIN, !digitalRead(LED_PIN));
    delay(100);
  }
}

void loop() {
  RCSOFTCHECK(rclc_executor_spin_some(&executor, RCL_MS_TO_NS(1)));
}

void period_change_callback(const void * msgin)
{  
  const std_msgs__msg__Int64 * period_msg = (const std_msgs__msg__Int64 *)msgin;
  int64_t old_period;
  int64_t new_period = period_msg->data;
  RCCHECK(rcl_timer_exchange_period(
    &timer, 
    RCL_MS_TO_NS(new_period),
    &old_period
    ));
}

void timer_callback(rcl_timer_t * timer, int64_t last_call_time)
{
  //Figure out what this does for now
  RCLC_UNUSED(last_call_time);

  if (timer != NULL)
  {
    mpu.getEvent(&a, &g, &temp);
    imu_msg.linear_acceleration.x = a.acceleration.x;
    imu_msg.linear_acceleration.y = a.acceleration.y;
    imu_msg.linear_acceleration.z = a.acceleration.z;

    imu_msg.angular_velocity.x = g.gyro.x;
    imu_msg.angular_velocity.y = g.gyro.y;
    imu_msg.angular_velocity.z = g.gyro.z;
    RCSOFTCHECK(rcl_publish(&publisher, &imu_msg, NULL));
  }
}

void motor_callback(rcl_timer_t * timer, int64_t last_call_time)
{
  RCLC_UNUSED(last_call_time);

  if (timer != NULL)
  {
    if ((last_cmd_vel_time - millisPassed) > motor_timeout)
    {
    
    }
  }
}

void setup() {
  set_microros_transports();
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, HIGH);  
  
  delay(2000);

  allocator = rcl_get_default_allocator();

  RCCHECK(rclc_support_init(&support, 0, NULL, &allocator));

  RCCHECK(rclc_node_init_default(&node, "balancing", "", &support));

  RCCHECK(rclc_subscription_init_default(
    &subscriber,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int64),
    "/balancing/imu/period"));

  RCCHECK(rclc_publisher_init_default(
    &publisher,
    &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(sensor_msgs, msg, Imu),
    "/balancing/imu/data_raw"));
    
  const unsigned int timer_timeout = 10;
  RCCHECK(rclc_timer_init_default(
    &timer,
    &support,
    RCL_MS_TO_NS(timer_timeout),
    timer_callback));

  // handler for running motors

  RCCHECK(rclc_timer_init_default(
    &motor_timer,
    &support,
    RCL_MS_TO_NS(motor_period),
    timer_callback));

  RCCHECK(rclc_executor_init(&executor, &support.context, 1, &allocator));
  RCCHECK(rclc_executor_add_timer(&executor, &timer));
  RCCHECK(rclc_executor_add_subscription(&executor, &subscriber, &period_msg, &period_change_callback, ON_NEW_DATA));

  if (!mpu.begin())
  {
    error_loop();
  }
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
}
