/**
 * Created by nlazic on 12/25/2017.
 */
package matf.beograd.master.nenadlazic.rpidroid_robot;

import android.content.Context;
import android.util.Log;
import android.widget.Toast;

import 	java.util.regex.Pattern;
import 	java.util.regex.Matcher;

class Utils {
    //HTTP response code
    public static enum HttpResponseCode {
        RPi_HTTP_OK,
        RPi_NOT_FOUND,
        RPi_UNDEFINED
    }

    //All possible directions of movement
    public static enum Direction {
        INVALID,
        STAND,
        GO_AHEAD,
        GO_SEMI_LEFT_AHEAD,
        GO_SEMI_RIGHT_AHEAD,
        GO_LEFT,
        GO_RIGHT,
        GO_BACK,
        GO_SEMI_LEFT_BACK,
        GO_SEMI_RIGHT_BACK,
        MAX
    }

    //Message type in request
    public static enum MessageType {
        RPi_MSG_DIRECTION,
        RPi_MSG_CONNECTING,
        RPi_MSG_DISCONNECTING,
        RPi_MSG_AUTO_MODE,
        RPi_MSG_UNDEFINED
    }

    public interface  OnResponseListener<T>{
        public void onSuccess(T object);
        public void onFailure(Exception e);
    }

    public static boolean isIpAddress(String ipAddress) {
        String IPADDRESS_PATTERN = "^([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\." +
                "([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\." +
                "([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\." +
                "([01]?\\d\\d?|2[0-4]\\d|25[0-5])$";
        Pattern pattern = Pattern.compile(IPADDRESS_PATTERN);
        Matcher matcher = pattern.matcher(ipAddress);
        return matcher.matches();
    }

    public static void RPiToastLog(String s, Context cnt){
        if(GlobalContextApplication.mToastLogEnabled) {
            CharSequence text = "connectingStart!";
            int duration = Toast.LENGTH_SHORT;
            Toast toast = Toast.makeText(cnt, s, duration);
            toast.show();
        }
    }

    public static void RPiAndroidLog(String s){
        if(GlobalContextApplication.mAndroidLogEnabled){
            Log.d("RPiDroid", s);
        }
    }

}
