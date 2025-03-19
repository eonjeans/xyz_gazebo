#include "rclcpp/rclcpp.hpp"
#include "gazebo_msgs/msg/model_states.hpp"

class IntegratedMainNode : public rclcpp::Node
{
public:
    IntegratedMainNode() : Node("integrated_main")
    {
        // Gazebo의 model_states 토픽 구독
        subscription_ = this->create_subscription<gazebo_msgs::msg::ModelStates>(
            "/gazebo/model_states", 10,
            std::bind(&IntegratedMainNode::modelStatesCallback, this, std::placeholders::_1)
        );

        RCLCPP_INFO(this->get_logger(), "integrated_main 노드 시작됨!");
    }

private:
    void modelStatesCallback(const gazebo_msgs::msg::ModelStates::SharedPtr msg)
    {
        // 모델 이름이 "box"인 경우를 찾음
        for (size_t i = 0; i < msg->name.size(); ++i)
        {
            if (msg->name[i] == "box")
            {
                auto position = msg->pose[i].position;

                RCLCPP_INFO(this->get_logger(),
                    "Box 위치 -> x: %.2f, y: %.2f, z: %.2f",
                    position.x, position.y, position.z);
            }
        }
    }

    rclcpp::Subscription<gazebo_msgs::msg::ModelStates>::SharedPtr subscription_;
};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<IntegratedMainNode>());
    rclcpp::shutdown();
    return 0;
}
