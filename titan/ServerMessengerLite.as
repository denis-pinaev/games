package common
{
    import common.adobe.*;
    import flash.events.*;
    import flash.net.*;
    import mx.utils.*;
    import platform.*;

    public class ServerMessengerLite extends EventDispatcher
    {
        public var serverUrl:String;
        public var sessionReqNN:int = 0;
        public static const COMMAND_PATH:String = "/server.php";
        static const _silentRequests:Array = ["getNewMessages"];
        static const _binaryRequests:Array = ["saveBattleReplay"];

        public function ServerMessengerLite()
        {
            return;
        }// end function

        public function createLoader(id:Number, request:Object, userData:Object) : CustomDynamicURLLoader
        {
            var _loc_4:* = new CustomDynamicURLLoader();
            _loc_4["requestName"] = request["request"];
            _loc_4["request"] = request;
            _loc_4["userData"] = userData;
            _loc_4["requestId"] = id;
            return _loc_4;
        }// end function

        public function load(loader:CustomDynamicURLLoader, request:Object) : void
        {
            var _loc_5:URLRequest = null;
            var _loc_6:URLVariables = null;
            var _loc_7:String = null;
            var _loc_3:* = new Date().toTimeString();
            _loc_3 = _loc_3.substring(0, _loc_3.length - 8);
            var _loc_4:* = this.serverUrl + COMMAND_PATH;
            if (request.method)
            {
            }
            if (request.method == "POST")
            {
                _loc_5 = new URLRequest(_loc_4);
                _loc_5.method = URLRequestMethod.POST;
                _loc_6 = new URLVariables();
                for (_loc_7 in request)
                {
                    
                    _loc_6[_loc_7] = encodeURIComponent(request[_loc_7]);
                }
                _loc_5.data = _loc_6;
                if (_silentRequests.indexOf(request.request) < 0)
                {
                    trace("(" + loader["requestId"] + "): POST REQUEST:  " + _loc_3 + " " + _loc_4 + this.createPathStringFromParams(request));
                }
            }
            else
            {
                _loc_4 = _loc_4 + this.createPathStringFromParams(request);
                if (_silentRequests.indexOf(request.request) < 0)
                {
                    trace("(" + loader["requestId"] + "): REQUEST:  " + _loc_3 + " " + _loc_4);
                }
                _loc_5 = new URLRequest(_loc_4);
            }
            loader.load(_loc_5);
            return;
        }// end function

        public function oneWayRequest(request:Object) : void
        {
            request = Platform.wrapper.addServerRequestParams(request);
            var _loc_2:* = this.createLoader(-1, request, null);
            this.load(_loc_2, request);
            return;
        }// end function

        private function createPathStringFromParams(request:Object) : String
        {
            var _loc_4:String = null;
            var _loc_5:String = null;
            var _loc_2:String = "";
            request.random = int(Math.random() * 1000000000);
            var _loc_6:String = this;
            _loc_6.sessionReqNN = ++this.sessionReqNN;
            request.tNN = ++this.sessionReqNN;
            var _loc_3:Array = [];
            for (_loc_4 in request)
            {
                
                _loc_3.push(_loc_4 + "=" + request[_loc_4]);
            }
            _loc_3.sort();
            _loc_5 = _loc_3.join("");
            request.tKey = MD5.hash(_loc_5);
            _loc_2 = "?" + URLUtil.objectToString(request, "&", true);
            return _loc_2;
        }// end function

    }
}
