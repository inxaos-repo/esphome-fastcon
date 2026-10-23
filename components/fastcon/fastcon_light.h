#pragma once

#include <array>
#include <vector>
#include "esphome/core/component.h"
#include "esphome/components/light/light_output.h"
#include "fastcon_controller.h"

namespace esphome
{
    namespace fastcon
    {
        enum class LightState
        {
            OFF,
            WARM_WHITE,
            RGB
        };

        class FastconLight : public Component, public light::LightOutput
        {
        public:
            FastconLight(uint8_t light_id) : light_id_(light_id) {}

            void setup() override;
            light::LightTraits get_traits() override;
            void write_state(light::LightState *state) override;
            void set_controller(FastconController *controller);
            void set_white_mode(uint8_t mode) { this->white_mode_ = static_cast<WhiteMode>(mode); }

        protected:
            FastconController *controller_{nullptr};
            uint8_t light_id_;
            WhiteMode white_mode_{WhiteMode::CCT};
        };
    } // namespace fastcon
} // namespace esphome
