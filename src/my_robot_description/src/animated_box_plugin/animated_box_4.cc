#include <boost/bind.hpp>
#include <gazebo/gazebo.hh>
#include <ignition/math.hh>
#include <gazebo/physics/physics.hh>
#include <gazebo/common/common.hh>
#include <stdio.h>

namespace gazebo
{
  class AnimatedBox4 : public ModelPlugin
  {
    public: void Load(physics::ModelPtr _parent, sdf::ElementPtr /*_sdf*/)
    {
      // Store the pointer to the model
      this->model = _parent;

      // ✅ 애니메이션 시간은 그대로 (6초 반복)
      gazebo::common::PoseAnimationPtr anim(
        new gazebo::common::PoseAnimation("test", 6.0, true)
      );

      gazebo::common::PoseKeyFrame *key;

      // ✅ 시작 위치: x=-3, y=-3
      key = anim->CreateKeyFrame(0);
      key->Translation(ignition::math::Vector3d(-3, -3, 0));
      key->Rotation(ignition::math::Quaterniond(0, 0, 0));

      // ✅ 1초 후: y=-2.5
      key = anim->CreateKeyFrame(1.0);
      key->Translation(ignition::math::Vector3d(-3, -2.5, 0));
      key->Rotation(ignition::math::Quaterniond(0, 0, 0));

      // ✅ 2초 후: y=-2
      key = anim->CreateKeyFrame(2.0);
      key->Translation(ignition::math::Vector3d(-3, -2, 0));
      key->Rotation(ignition::math::Quaterniond(0, 0, 0));

      // ✅ 3초 후: y=-1.5
      key = anim->CreateKeyFrame(3.0);
      key->Translation(ignition::math::Vector3d(-3, -1.5, 0));
      key->Rotation(ignition::math::Quaterniond(0, 0, 0));

      // ✅ 4초 후: y=-2
      key = anim->CreateKeyFrame(4.0);
      key->Translation(ignition::math::Vector3d(-3, -2, 0));
      key->Rotation(ignition::math::Quaterniond(0, 0, 0));

      // ✅ 5초 후: y=-2.5
      key = anim->CreateKeyFrame(5.0);
      key->Translation(ignition::math::Vector3d(-3, -2.5, 0));
      key->Rotation(ignition::math::Quaterniond(0, 0, 0));

      // ✅ 6초 후: y=-3 (시작 위치로 복귀)
      key = anim->CreateKeyFrame(6.0);
      key->Translation(ignition::math::Vector3d(-3, -3, 0));
      key->Rotation(ignition::math::Quaterniond(0, 0, 0));

      // ✅ 애니메이션 적용
      _parent->SetAnimation(anim);
    }

    // Pointer to the model
    private: physics::ModelPtr model;

    // Pointer to the update event connection (현재 사용하지 않음)
    private: event::ConnectionPtr updateConnection;
  };

  // Register this plugin with the simulator
  GZ_REGISTER_MODEL_PLUGIN(AnimatedBox4)
}
