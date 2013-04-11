import java.io.IOException;
import java.util.Iterator;

import com.likethecolor.alchemy.api.Client;
import com.likethecolor.alchemy.api.call.AbstractCall;
import com.likethecolor.alchemy.api.call.SentimentCall;
import com.likethecolor.alchemy.api.call.type.CallTypeUrl;
import com.likethecolor.alchemy.api.entity.Response;
import com.likethecolor.alchemy.api.entity.SentimentAlchemyEntity;


public class MainAlchemyAPI {

	/**
	 * @param args
	 * @throws IOException 
	 */
	public static void main(String[] args) throws IOException {
	    final Client client = new Client("/alchemy-api-key.txt");

	    final AbstractCall call = new SentimentCall(new CallTypeUrl("http://www.answers.com/article/3b7a1506797deda268075f0886eac4d8"));
	    final Response response = client.call(call);

	    System.out.println("Language: " + response.getLanguage());
	    System.out.println("Status: " + response.getStatus());
	    System.out.println("Status Info: " + response.getStatusInfo());
	    System.out.println("Text: " + response.getText());
	    System.out.println("Usage: " + response.getUsage());
	    System.out.println("URL: " + response.getURL());

	    SentimentAlchemyEntity entity;
	    final Iterator<SentimentAlchemyEntity> iter = response.iterator();
	    while(iter.hasNext()) {
	      entity = iter.next();
	      System.out.println("isMixed: " + (entity.isMixed() ? "true" : "false"));
	      System.out.println("Score: " + entity.getScore());
	      System.out.println("Type: " + entity.getType());
	    }
	    
	}

}
