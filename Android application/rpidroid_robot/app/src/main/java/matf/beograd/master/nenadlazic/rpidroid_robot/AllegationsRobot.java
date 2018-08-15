package matf.beograd.master.nenadlazic.rpidroid_robot;

import android.app.Activity;
import android.content.ComponentName;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.ServiceConnection;
import android.content.SharedPreferences;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.IBinder;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.SimpleAdapter;
import android.widget.TextView;
import android.widget.Toast;

public class AllegationsRobot extends AppCompatActivity implements SensorEventListener, CommunicationService.ServiceCallbacks{

    //Handlers for UI components
    private ImageView iv;
    private TextView tv;
    private Button btnAutoMode;
    private Button btnStop;

    //Giroscope
    private Sensor giroscopeSensor;
    private SensorManager sm;

    //Comunications with RPi
    private Intent serviceIntent;
    private CommunicationService comService;
    private ServiceConnection mConnection;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_allegations_robot);

        iv = (ImageView)findViewById(R.id.direction_iv);
        tv = (TextView)findViewById(R.id.textView2);
        btnAutoMode = (Button)findViewById(R.id.button);
        btnStop = (Button)findViewById(R.id.button2);

        sm = (SensorManager)getSystemService(SENSOR_SERVICE);
        giroscopeSensor = sm.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
        sm.registerListener(this, giroscopeSensor, SensorManager.SENSOR_DELAY_NORMAL);

        btnAutoMode.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                tv.setText("RPiDROID: prepreka na putu");
                iv.setImageResource(R.drawable.warning);
            }
        });

        btnStop.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                tv.setText("RPiDROID: autonomni mod ukljucen");
                iv.setImageResource(R.drawable.autondriv);
            }
        });

    }

    @Override
    protected void onStart() {
        super.onStart();

        serviceIntent = new Intent(AllegationsRobot.this, CommunicationService.class);
        startService(serviceIntent);
        mConnection = new ServiceConnection() {
            @Override
            public void onServiceConnected(ComponentName componentName, IBinder iBinder) {
                CommunicationService.LocalBinder binder = (CommunicationService.LocalBinder) iBinder;
                comService = binder.getServerInstance();
                comService.registerClient(AllegationsRobot.this);
                SharedPreferences prefs = getSharedPreferences(GlobalContextApplication.IP_ADDRESS_PREFS_NAME, MODE_PRIVATE);
                String mIpAddress = prefs.getString(GlobalContextApplication.mPrefsName,"default_return_value");
                comService.saveIpAddress(mIpAddress);
                comService.saveAppContext(getApplicationContext());
                Utils.RPiAndroidLog("CommunicationService connected");
            }

            @Override
            public void onServiceDisconnected(ComponentName componentName) {
                Utils.RPiAndroidLog("CommunicationService disconnected");
            }
        };

        bindService(serviceIntent, mConnection, Context.BIND_AUTO_CREATE); //Binding to the service!
    }

    @Override
    protected void onResume() {
        super.onResume();
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        stopService(serviceIntent);
    }


    //Implementation of interface SensorEventListener
    @Override
    public void onSensorChanged(SensorEvent event) {
        float x = event.values[0];
        float y = event.values[1];
        float z = event.values[2];

        boolean retState = false;

        if(x>-1 && x<1 && y>-1 && y<1){
            tv.setText("RPiDROID: stojim");
            iv.setImageResource(R.drawable.and);
            if(comService != null) {
                comService.inform_of_change("stand", Utils.MessageType.RPi_MSG_DIRECTION);
            }
        }

        if(x>-1 && x<1 && y<-1){
            tv.setText("RPiDROID: idem napred");
            iv.setImageResource(R.drawable.strelica_pravo);
            if(comService != null) {
                comService.inform_of_change("go_ahead", Utils.MessageType.RPi_MSG_DIRECTION);
            }
        }

        if(x>-1 && x<1 && y>1){
            tv.setText("RPiDROID: idem nazad");
            iv.setImageResource(R.drawable.strelica_nazad);
            if(comService != null) {
                comService.inform_of_change("go_back",Utils.MessageType.RPi_MSG_DIRECTION);
            }
        }

        if(x>1 && y>-1 && y<1){
            tv.setText("RPiDROID: idem levo");
            iv.setImageResource(R.drawable.strelica_levo);
            if(comService != null) {
                comService.inform_of_change("go_left",Utils.MessageType.RPi_MSG_DIRECTION);
            }
        }

        if(x<-1 && y>-1 && y<1){
            tv.setText("RPiDROID: idem desno");
            iv.setImageResource(R.drawable.strelica_desno);
            if(comService != null) {
                comService.inform_of_change("go_right", Utils.MessageType.RPi_MSG_DIRECTION);
            }
        }

        if(x>1 && y>1){
//            iv.setImageResource(R.drawable.strelica_levo);
            if(comService != null) {
                comService.inform_of_change("go_b_left",Utils.MessageType.RPi_MSG_DIRECTION);
            }

        }

        if(x<-1 && y>1){
//            iv.setImageResource(R.drawable.strelica_desno);
            if(comService != null) {
                comService.inform_of_change("go_b_right", Utils.MessageType.RPi_MSG_DIRECTION);
            }

        }
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {
        //TODO
    }

    @Override
    public void CommunicationServiceCallbacks() {
    }
}
