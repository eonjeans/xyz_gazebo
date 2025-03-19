#include <gazebo/gazebo.hh>
#include <ignition/math.hh>
#include <gazebo/physics/physics.hh>
#include <gazebo/common/common.hh>
#include <stdio.h>

namespace gazebo
{
  class AnimatedBox2 : public ModelPlugin
  {
    public: void Load(physics::ModelPtr _parent, sdf::ElementPtr /*_sdf*/)
    {
      // Store the pointer to the model
      this->model = _parent;

      // ✅ Create the animation
      gazebo::common::PoseAnimationPtr anim(
        new gazebo::common::PoseAnimation("test", 12.0, true) // 12초 루프 애니메이션
      );

      gazebo::common::PoseKeyFrame *key;

      // ✅ 시작 위치 (x=2, y=0)
      key = anim->CreateKeyFrame(0);
      key->Translation(ignition::math::Vector3d(2, 0, 0));
      key->Rotation(ignition::math::Quaterniond(0, 0, 0));

      // ✅ 2초 후 (y=1)
      key = anim->CreateKeyFrame(2.0);
      key->Translation(ignition::math::Vector3d(2, 1, 0));
      key->Rotation(ignition::math::Quaterniond(0, 0, 0));

      // ✅ 4초 후 (y=2)
      key = anim->CreateKeyFrame(4.0);
      key->Translation(ignition::math::Vector3d(2, 2, 0));
      key->Rotation(ignition::math::Quaterniond(0, 0, 0));

      // ✅ 6초 후 (y=3)
      key = anim->CreateKeyFrame(6.0);
      key->Translation(ignition::math::Vector3d(2, 3, 0));
      key->Rotation(ignition::math::Quaterniond(0, 0, 0));

      // ✅ 8초 후 (y=2)
      key = anim->CreateKeyFrame(8.0);
      key->Translation(ignition::math::Vector3d(2, 2, 0));
      key->Rotation(ignition::math::Quaterniond(0, 0, 0));

      // ✅ 10초 후 (y=1)
      key = anim->CreateKeyFrame(10.0);
      key->Translation(ignition::math::Vector3d(2, 1, 0));
      key->Rotation(ignition::math::Quaterniond(0, 0, 0));

      // ✅ 12초 후 (y=0, 시작 위치로 복귀)
      key = anim->CreateKeyFrame(12.0);
      key->Translation(ignition::math::Vector3d(2, 0, 0));
      key->Rotation(ignition::math::Quaterniond(0, 0, 0));

      // ✅ 애니메이션 설정 적용
      _parent->SetAnimation(anim);
    }

    // Pointer to the model
    private: physics::ModelPtr model;

    // Pointer to the update event connection
    private: event::ConnectionPtr updateConnection;
  };

  // Register this plugin with the simulator
  GZ_REGISTER_MODEL_PLUGIN(AnimatedBox2)
}
