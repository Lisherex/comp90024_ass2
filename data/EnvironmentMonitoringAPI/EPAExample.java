import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.util.HashMap;
import java.util.Map;
import java.io.UnsupportedEncodingException;
import java.io.DataInputStream;
import java.io.InputStream;
import java.io.FileInputStream;

public class EPAExample {

  public static void main(String[] args) {
    try {
        String urlString = "https://gateway.api.epa.vic.gov.au/environmentMonitoring/v1/sites/63a73778-4244-481b-82d9-3a7c416832eb/parameters?since=2022-05-03T02:00:00Z&until=2022-05-04T03:00:00Z&interval=1HR_AV";
        URL url = new URL(urlString);
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();

        //Request headers
    connection.setRequestProperty("Cache-Control", "no-cache");
    
    connection.setRequestProperty("X-API-Key", "7d3c9901e475402f844691c300e4efa8");
    
        connection.setRequestMethod("GET");

        int status = connection.getResponseCode();
        System.out.println(status);

        BufferedReader in = new BufferedReader(
            new InputStreamReader(connection.getInputStream())
        );
        String inputLine;
        StringBuffer content = new StringBuffer();
        while ((inputLine = in.readLine()) != null) {
            content.append(inputLine);
        }
        in.close();
        System.out.println(content);

        connection.disconnect();
    } catch (Exception ex) {
      System.out.print("exception:" + ex.getMessage());
    }
  }
}