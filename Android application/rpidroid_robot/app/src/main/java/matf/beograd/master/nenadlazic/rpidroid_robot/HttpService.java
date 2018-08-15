/**
 * Created by nlazic on 19.4.17.
 */
package matf.beograd.master.nenadlazic.rpidroid_robot;

import android.os.AsyncTask;
import android.content.Context;
import android.util.Log;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;


public class HttpService extends AsyncTask<Void, Void, String> {

    private Utils.OnResponseListener<String> mCallback; //callback for http response
    private Context mContext;
    private String mUrl;
    private String mValue;
    private Exception mException;
    private int mResponseCode;
    private Utils.MessageType mMessageType;

    public HttpService(Context context, Utils.OnResponseListener callback, String ipAddress, String params, Utils.MessageType msgType) {
        mCallback = callback;
        mContext = context;
        mUrl = ipAddress;
        mValue = params;
        mException = null;
        mResponseCode  = HttpURLConnection.HTTP_UNAVAILABLE;
        mMessageType = msgType;
    }

    @Override
    protected String doInBackground(Void... params) {
        HttpURLConnection connection = null;
        String subPage = "";
        mResponseCode = HttpURLConnection.HTTP_UNAVAILABLE;

        try {
            long requestStartTime = System.nanoTime();
            //Create connection and set params
            URL url = new URL("http://192.168.1.100:5000");
            connection = (HttpURLConnection) url.openConnection();
            connection.setUseCaches(false);
            connection.setConnectTimeout(500); //set timeout to 0.5 seconds


            //Send request
            String parametriZaSlanje = "{\"message_type\":\""+mMessageType.name()+"\",\"value\":\""+mValue+"\"}";;
            connection.setRequestProperty("Content-Length",Integer.toString(parametriZaSlanje.getBytes().length));
            connection.setRequestProperty("Content-Language", "en-US");
            connection.setRequestProperty("Content-Type", "application/json; charset=UTF-8");
            connection.setDoOutput(true);
            connection.setDoInput(true);
            connection.setRequestMethod("POST");


            OutputStream wr = connection.getOutputStream();
            wr.write(parametriZaSlanje.getBytes("UTF-8"));
            wr.close();

            //Get Response
            mResponseCode = connection.getResponseCode();

            //Request duration
            long requestEndTime = System.nanoTime();
            long durationRequest = (requestEndTime - requestStartTime) / 1000;
            Log.d("rpi HTTP request duration","duration: "+durationRequest);


            if(mResponseCode == HttpURLConnection.HTTP_OK){
                InputStream is = connection.getInputStream();
                BufferedReader rd = new BufferedReader(new InputStreamReader(is));
                StringBuilder response = new StringBuilder();
                String line;

                while ((line = rd.readLine()) != null) {
                    response.append(line);
                    response.append('\r');
                }
                rd.close();
                return response.toString(); //This return value catch in onPostExecute
            } else {
                Log.d("HttpService", "Response code: "+mResponseCode);
            }

            connection.disconnect();
        } catch (Exception e) {
            mException = e;
            e.printStackTrace();
            return null;
        } finally {
            if (connection != null) {
                connection.disconnect();
            }
        }

        return null;
    }


    //This function called when doInBackground finished. From here notify sender.
    @Override
    protected void onPostExecute(String s) {
        super.onPostExecute(s);

        if (mCallback != null && s != null && mException == null) {
            if (mResponseCode == HttpURLConnection.HTTP_OK) {
                mCallback.onSuccess(s);
            } else {
                mCallback.onFailure(mException);
            }
        }
    }

    //api koji mora da implementira svaki korisnik servisa
    public interface HttpServiceCallbacks {
        void callback1();
        void callback2();
        void callback3();
        void callback4();

    }
}
