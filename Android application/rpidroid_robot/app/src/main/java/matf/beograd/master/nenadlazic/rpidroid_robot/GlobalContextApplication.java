/**
 * Created by rtrk on 12/26/17.
 */
package matf.beograd.master.nenadlazic.rpidroid_robot;

import android.app.Application;
import android.content.res.Configuration;

public class GlobalContextApplication extends Application {

    //TODO here share global resource and handlers
    public static boolean mToastLogEnabled = false;
    public static boolean mAndroidLogEnabled = true;
    public static final String IP_ADDRESS_PREFS_NAME = "IpAddressPrefsName";
    public static final String mPrefsName = "ip_address";


    // Called when the application is starting, before any other application objects have been created.
    // Overriding this method is totally optional!
    @Override
    public void onCreate() {
        super.onCreate();
        // Required initialization logic here!
    }

    // Called by the system when the device configuration changes while your component is running.
    // Overriding this method is totally optional!
    @Override
    public void onConfigurationChanged(Configuration newConfig) {
        super.onConfigurationChanged(newConfig);
    }

    // This is called when the overall system is running low on memory,
    // and would like actively running processes to tighten their belts.
    // Overriding this method is totally optional!
    @Override
    public void onLowMemory() {
        super.onLowMemory();
    }
}
