#include <boost/bind.hpp>
#include <gazebo/gazebo.hh>
#include <ignition/math.hh>
#include <gazebo/physics/physics.hh>
#include <gazebo/common/common.hh>
#include <stdio.h>

namespace gazebo
{
  class AnimatedBox3 : public ModelPlugin
  {
    public: void Load(physics::ModelPtr _parent, sdf::ElementPtr /*_sdf*/)
    {
      // Store the pointer to the model
      this->model = _parent;

      // ✅ 애니메이션 생성 (8초 반복)
      gazebo::common::PoseAnimationPtr anim(
        new gazebo::common::PoseAnimation("test", 8.0, true)
      );

      gazebo::common::PoseKeyFrame *key;

      // ✅ 시작 지점 (x: 3.0, y: -3.0)
      key = anim->CreateKeyFrame(0.0);
      key->Translation(ignition::math::Vector3d(3.0, -3.0, 0));
      key->Rotation(ignition::math::Quaterniond(0, 0, 0));

      // ✅ 2초 후 (y 증가: -1.5)
      key = anim->CreateKeyFrame(2.0);
      key->Translation(ignition::math::Vector3d(3.0, -1.5, 0));
      key->Rotation(ignition::math::Quaterniond(0, 0, 0));

      // ✅ 4초 후 (y 최대값: +3.0)
      key = anim->CreateKeyFrame(4.0);
      key->Translation(ignition::math::Vector3d(3.0, 3.0, 0));
      key->Rotation(ignition::math::Quaterniond(0, 0, 0));

      // ✅ 6초 후 (y 다시 감소: -1.5)
      key = anim->CreateKeyFrame(6.0);
      key->Translation(ignition::math::Vector3d(3.0, -1.5, 0));
      key->Rotation(ignition::math::Quaterniond(0, 0, 0));

      // ✅ 8초 후 (시작 위치로 복귀: -3.0)
      key = anim->CreateKeyFrame(8.0);
      key->Translation(ignition::math::Vector3d(3.0, -3.0, 0));
      key->Rotation(ignition::math::Quaterniond(0, 0, 0));

      // ✅ 애니메이션 적용
      _parent->SetAnimation(anim);
    }

    // Pointer to the model
    private: physics::ModelPtr model;

    // Pointer to the update event connection (현재 사용 안 함)
    private: event::ConnectionPtr updateConnection;
  };

  // Register this plugin with the simulator
  GZ_REGISTER_MODEL_PLUGIN(AnimatedBox3)
}
