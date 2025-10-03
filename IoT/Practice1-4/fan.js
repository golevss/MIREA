defineRule("fan-control",{
    whenChanged: "wb-msw-v3_21/Current Motion",
        then : function (newValue, devName, cellName) {
            if (newValue > 1000){
                dev["load_control"]["L2"] = true;
            }else{
                dev["load_control"]["L2"] = false;
            }
        }
});
