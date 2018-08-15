package matf.beograd.master.nenadlazic.rpidroid_robot;

import android.app.Activity;
import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.os.Binder;
import android.os.IBinder;
import java.util.concurrent.locks.ReentrantReadWriteLock;

public class CommunicationService extends Service {
    private IBinder mBinder;
    private ServiceCallbacks activity;
    private ReentrantReadWriteLock rwlock = new ReentrantReadWriteLock(true);
    private String mHttpParams;
    private Utils.MessageType mHttpMessageType;
    private String mIpAddress;
    private Context mAppContext;
    private long mLastRequest;

    public CommunicationService() {
        mBinder = new LocalBinder();

        mHttpParams = "undefined";
        mHttpMessageType = Utils.MessageType.RPi_MSG_UNDEFINED;
        mLastRequest = 0;
    }

    public void registerClient(Activity activity)
    {
        this.activity = (ServiceCallbacks) activity;
    }

    public void saveIpAddress(String ip){
        Utils.RPiAndroidLog("Save IP address in Communication service");
        Utils.RPiAndroidLog("Save application context in Communication service");
        mIpAddress = new String(ip);
    }

    public void saveAppContext(Context cnt){
        mAppContext = cnt;
    }

    public class LocalBinder extends Binder {
        public CommunicationService getServerInstance()
        {
            return CommunicationService.this;
        }
    }

    //This funcion is called from AllegationsRobot when SensorEvent received
    public void inform_of_change(String params, Utils.MessageType messageType) {
        rwlock.writeLock().lock();
        try{
            Utils.RPiAndroidLog("WRITE LOCKED");
            mHttpParams = new String(params);
            mHttpMessageType = messageType;
            Utils.RPiAndroidLog("inform_of_change: params="+params+" msg_type="+messageType.name());
            sendRequest();
        } finally {
            rwlock.writeLock().unlock();
            Utils.RPiAndroidLog("WRITE UNLOCKED");
        }
    }

    public void sendRequest() {
        long currMs = System.currentTimeMillis();
        if(currMs - mLastRequest < 500){
            return;
        } else {
            mLastRequest = currMs;
        }
        HttpService httpService = new HttpService(getApplicationContext(), new Utils.OnResponseListener<String>() {
            @Override
            public void onSuccess(String object) {
                Utils.RPiToastLog("REQUEST SUCCESS", mAppContext);
            }

            @Override
            public void onFailure(Exception e) {
                Utils.RPiToastLog("REQUEST FAILURE", mAppContext);
            }
        }, mIpAddress,mHttpParams,mHttpMessageType);

        httpService.execute();
    }

    @Override
    public IBinder onBind(Intent intent) {
        return mBinder;
    }

    public interface ServiceCallbacks {
        void CommunicationServiceCallbacks();
    }
}
