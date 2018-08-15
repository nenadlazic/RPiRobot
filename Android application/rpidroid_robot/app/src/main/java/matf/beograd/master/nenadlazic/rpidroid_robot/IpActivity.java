/**
 * Created by nlazic on 12/25/2017.
 */
package matf.beograd.master.nenadlazic.rpidroid_robot;

import android.content.Context;
import android.graphics.drawable.AnimationDrawable;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.content.SharedPreferences;
import android.os.Handler;
import android.content.Intent;

//VOLLEY work ok***********************************************************************************
//import com.android.volley.Request;
//import com.android.volley.Response;
//import com.android.volley.VolleyError;
//import com.android.volley.toolbox.StringRequest;
//************************************************************************************************


public class IpActivity extends AppCompatActivity {

    //Handlers for loading animation during connecting
    AnimationDrawable animation;
    ImageView loading;

    //Handler for connection button
    Button btnConnect;
    //Handlers for field IP address
    EditText editText;

    //Volley handler which will be used throughout the life cycle of the application
    //SingletonVolley volleyHandler;

    private boolean connected;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_ip);

        //Prepare loading animation
        loading = (ImageView) findViewById(R.id.imageView2);
        animation = (AnimationDrawable) loading.getDrawable();

        //Get handlers for UI components
        btnConnect = (Button) findViewById(R.id.button_ip);
        editText = (EditText) findViewById(R.id.edit_ip);

        connected = false;

        String nameMethod = new Object(){}.getClass().getEnclosingMethod().getName();
        Utils.RPiToastLog(nameMethod, getApplicationContext());
        Utils.RPiAndroidLog(nameMethod);

    }

    @Override
    protected void onStart() {
        super.onStart();

        String nameMethod = new Object(){}.getClass().getEnclosingMethod().getName();
        Utils.RPiToastLog(nameMethod, getApplicationContext());
        Utils.RPiAndroidLog(nameMethod);
    }

    @Override
    protected void onResume() {
        super.onResume();

        String nameMethod = new Object(){}.getClass().getEnclosingMethod().getName();
        Utils.RPiToastLog(nameMethod, getApplicationContext());
        Utils.RPiAndroidLog(nameMethod);
    }

    @Override
    protected void onPause() {
        super.onPause();

        String nameMethod = new Object(){}.getClass().getEnclosingMethod().getName();
        Utils.RPiToastLog(nameMethod, getApplicationContext());
        Utils.RPiAndroidLog(nameMethod);
    }

    @Override
    protected void onStop() {
        super.onStop();

        String nameMethod = new Object(){}.getClass().getEnclosingMethod().getName();
        Utils.RPiToastLog(nameMethod, getApplicationContext());
        Utils.RPiAndroidLog(nameMethod);
    }

    @Override
    protected void onRestart() {
        super.onRestart();

        String nameMethod = new Object(){}.getClass().getEnclosingMethod().getName();
        Utils.RPiToastLog(nameMethod, getApplicationContext());
        Utils.RPiAndroidLog(nameMethod);

        if(connected == true){
            final Handler handler = new Handler();
            handler.postDelayed(new Runnable() {
                @Override
                public void run() {
                    //Do something after 3s
                    //sent intent
                    Intent intent = new Intent(getApplicationContext(), AllegationsRobot.class);
                    startActivity(intent);
                }
            }, 3000);
        }
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();

        String nameMethod = new Object(){}.getClass().getEnclosingMethod().getName();
        Utils.RPiToastLog(nameMethod, getApplicationContext());
        Utils.RPiAndroidLog(nameMethod);
    }

    //Connection button listener
    public void connectingStart(final View v) {
        //Check if the IP address field is correctly filled then create request and start animation
        final String sIpAddress = editText.getText().toString();
        if (Utils.isIpAddress(sIpAddress)) {
            startAnimation(v);
            btnConnect.setClickable(false);

            String nameMethod = new Object(){}.getClass().getEnclosingMethod().getName();
            Utils.RPiToastLog(nameMethod, getApplicationContext());
            Utils.RPiAndroidLog(nameMethod);

            HttpService httpService = new HttpService(getApplicationContext(), new Utils.OnResponseListener<String>() {
                @Override
                public void onSuccess(String object) {

                    String nameMethod = new Object(){}.getClass().getEnclosingMethod().getName();
                    Utils.RPiToastLog(object.toString(), getApplicationContext());
                    Utils.RPiAndroidLog(nameMethod);
                    connected = true;

                    stopAnimation(v, Utils.HttpResponseCode.RPi_HTTP_OK);


                    //Save ip address in shared prefference
                    SharedPreferences settings = getSharedPreferences(GlobalContextApplication.IP_ADDRESS_PREFS_NAME, Context.MODE_PRIVATE);
                    SharedPreferences.Editor editor = getSharedPreferences(GlobalContextApplication.IP_ADDRESS_PREFS_NAME, MODE_PRIVATE).edit();
                    editor.putString(GlobalContextApplication.mPrefsName, sIpAddress);
                    editor.putInt("something",1);
                    editor.apply();

                    //TODO use in another activity
                    //Read ip address from shared pref
                    SharedPreferences prefs = getSharedPreferences(GlobalContextApplication.IP_ADDRESS_PREFS_NAME, MODE_PRIVATE);
                    String sIpAdRestore = prefs.getString(GlobalContextApplication.mPrefsName,"default_return_value");
                    Utils.RPiAndroidLog("From shared pref: "+sIpAddress);
                    Utils.RPiToastLog(sIpAddress,getApplicationContext());

                    //TODO intent for new activity
                    final Handler handler = new Handler();
                    handler.postDelayed(new Runnable() {
                        @Override
                        public void run() {
                            //Do something after 100ms
                            //sent intent
                            Intent intent = new Intent(getApplicationContext(), AllegationsRobot.class);
                            startActivity(intent);
                        }
                    }, 3000);
                }

                @Override
                public void onFailure(Exception e) {
                    editText.setText("exception");

                    String nameMethod = new Object(){}.getClass().getEnclosingMethod().getName();
                    Utils.RPiToastLog(nameMethod, getApplicationContext());
                    Utils.RPiAndroidLog(nameMethod);

                    stopAnimation(v, Utils.HttpResponseCode.RPi_UNDEFINED);
                    btnConnect.setClickable(true);
                }
            }, sIpAddress,"connecting", Utils.MessageType.RPi_MSG_CONNECTING);

            httpService.execute();
        } else {
            stopAnimation(v, Utils.HttpResponseCode.RPi_UNDEFINED);
        }
    }

    //Starting loading animation
    public void startAnimation(View v) {
        int retVisibility = loading.getVisibility();
        if(retVisibility != View.VISIBLE) {
            loading.setVisibility(View.VISIBLE);
        } else {
            loading.setImageResource(R.drawable.loading);
            animation = (AnimationDrawable) loading.getDrawable();
        }
        animation.start();
    }

    //Stopping loading animation
    public void stopAnimation(View v, Utils.HttpResponseCode response) {
        int retVisibility = loading.getVisibility();
        if(retVisibility != View.VISIBLE) {
            loading.setVisibility(View.VISIBLE);
        }

        animation.stop();
        if (response == Utils.HttpResponseCode.RPi_HTTP_OK) {
            loading.setImageResource(R.drawable.ok_img);
        } else {
            loading.setImageResource(R.drawable.notok_img);
        }
    }
}


//VOLLEY work ok***********************************************************************************
//            volleyHandler = new SingletonVolley(getApplicationContext());
//            String mUrlString = "192.168.1.102";
//            // Initialize a new StringRequest
//            StringRequest stringRequest = new StringRequest(
//                    Request.Method.GET,
//                    mUrlString,
//                    new Response.Listener<String>() {
//                        @Override
//                        public void onResponse(String response) {
//                            // Do something with response string
//                            //editText.setText(response.toString());
//                            stopAnimation(v, Utils.HttpResponseCode.RPi_HTTP_OK);
//                        }
//                    },
//                    new Response.ErrorListener() {
//                        @Override
//                        public void onErrorResponse(VolleyError error) {
//                            // Do something when get error
//                            //Snackbar.make(mCLayout, "Error...", Snackbar.LENGTH_LONG).show();
//                        }
//                    }
//            );
//            volleyHandler.addToRequestQueue(stringRequest);
//*************************************************************************************************
