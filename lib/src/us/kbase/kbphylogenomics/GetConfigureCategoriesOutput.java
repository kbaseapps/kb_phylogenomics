
package us.kbase.kbphylogenomics;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: get_configure_categories_Output</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "cats",
    "cat2name",
    "cat2group",
    "domfam2cat",
    "cat2domfams"
})
public class GetConfigureCategoriesOutput {

    @JsonProperty("cats")
    private List<String> cats;
    /**
     * <p>Original spec-file type: Cat2Name</p>
     * <pre>
     * category to name
     * </pre>
     * 
     */
    @JsonProperty("cat2name")
    private Cat2Name cat2name;
    /**
     * <p>Original spec-file type: Cat2Group</p>
     * <pre>
     * category to group
     * </pre>
     * 
     */
    @JsonProperty("cat2group")
    private Cat2Group cat2group;
    /**
     * <p>Original spec-file type: DomFam2Cat</p>
     * <pre>
     * domain family to category
     * </pre>
     * 
     */
    @JsonProperty("domfam2cat")
    private DomFam2Cat domfam2cat;
    /**
     * <p>Original spec-file type: Cat2DomFams</p>
     * <pre>
     * category to domain family
     * </pre>
     * 
     */
    @JsonProperty("cat2domfams")
    private Cat2DomFams cat2domfams;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("cats")
    public List<String> getCats() {
        return cats;
    }

    @JsonProperty("cats")
    public void setCats(List<String> cats) {
        this.cats = cats;
    }

    public GetConfigureCategoriesOutput withCats(List<String> cats) {
        this.cats = cats;
        return this;
    }

    /**
     * <p>Original spec-file type: Cat2Name</p>
     * <pre>
     * category to name
     * </pre>
     * 
     */
    @JsonProperty("cat2name")
    public Cat2Name getCat2name() {
        return cat2name;
    }

    /**
     * <p>Original spec-file type: Cat2Name</p>
     * <pre>
     * category to name
     * </pre>
     * 
     */
    @JsonProperty("cat2name")
    public void setCat2name(Cat2Name cat2name) {
        this.cat2name = cat2name;
    }

    public GetConfigureCategoriesOutput withCat2name(Cat2Name cat2name) {
        this.cat2name = cat2name;
        return this;
    }

    /**
     * <p>Original spec-file type: Cat2Group</p>
     * <pre>
     * category to group
     * </pre>
     * 
     */
    @JsonProperty("cat2group")
    public Cat2Group getCat2group() {
        return cat2group;
    }

    /**
     * <p>Original spec-file type: Cat2Group</p>
     * <pre>
     * category to group
     * </pre>
     * 
     */
    @JsonProperty("cat2group")
    public void setCat2group(Cat2Group cat2group) {
        this.cat2group = cat2group;
    }

    public GetConfigureCategoriesOutput withCat2group(Cat2Group cat2group) {
        this.cat2group = cat2group;
        return this;
    }

    /**
     * <p>Original spec-file type: DomFam2Cat</p>
     * <pre>
     * domain family to category
     * </pre>
     * 
     */
    @JsonProperty("domfam2cat")
    public DomFam2Cat getDomfam2cat() {
        return domfam2cat;
    }

    /**
     * <p>Original spec-file type: DomFam2Cat</p>
     * <pre>
     * domain family to category
     * </pre>
     * 
     */
    @JsonProperty("domfam2cat")
    public void setDomfam2cat(DomFam2Cat domfam2cat) {
        this.domfam2cat = domfam2cat;
    }

    public GetConfigureCategoriesOutput withDomfam2cat(DomFam2Cat domfam2cat) {
        this.domfam2cat = domfam2cat;
        return this;
    }

    /**
     * <p>Original spec-file type: Cat2DomFams</p>
     * <pre>
     * category to domain family
     * </pre>
     * 
     */
    @JsonProperty("cat2domfams")
    public Cat2DomFams getCat2domfams() {
        return cat2domfams;
    }

    /**
     * <p>Original spec-file type: Cat2DomFams</p>
     * <pre>
     * category to domain family
     * </pre>
     * 
     */
    @JsonProperty("cat2domfams")
    public void setCat2domfams(Cat2DomFams cat2domfams) {
        this.cat2domfams = cat2domfams;
    }

    public GetConfigureCategoriesOutput withCat2domfams(Cat2DomFams cat2domfams) {
        this.cat2domfams = cat2domfams;
        return this;
    }

    @JsonAnyGetter
    public Map<java.lang.String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(java.lang.String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public java.lang.String toString() {
        return ((((((((((((("GetConfigureCategoriesOutput"+" [cats=")+ cats)+", cat2name=")+ cat2name)+", cat2group=")+ cat2group)+", domfam2cat=")+ domfam2cat)+", cat2domfams=")+ cat2domfams)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
