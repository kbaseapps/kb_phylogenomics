
package us.kbase.kbphylogenomics;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: view_tree_Input</p>
 * <pre>
 * view_tree()
 * **
 * ** show a KBase Tree and make newick and images downloadable
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "workspace_name",
    "input_tree_ref",
    "desc",
    "show_genome_obj_name",
    "color_for_reference_genomes",
    "color_for_skeleton_genomes",
    "color_for_user_genomes",
    "tree_shape"
})
public class ViewTreeInput {

    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("input_tree_ref")
    private String inputTreeRef;
    @JsonProperty("desc")
    private String desc;
    @JsonProperty("show_genome_obj_name")
    private Long showGenomeObjName;
    @JsonProperty("color_for_reference_genomes")
    private String colorForReferenceGenomes;
    @JsonProperty("color_for_skeleton_genomes")
    private String colorForSkeletonGenomes;
    @JsonProperty("color_for_user_genomes")
    private String colorForUserGenomes;
    @JsonProperty("tree_shape")
    private String treeShape;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("workspace_name")
    public String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public ViewTreeInput withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("input_tree_ref")
    public String getInputTreeRef() {
        return inputTreeRef;
    }

    @JsonProperty("input_tree_ref")
    public void setInputTreeRef(String inputTreeRef) {
        this.inputTreeRef = inputTreeRef;
    }

    public ViewTreeInput withInputTreeRef(String inputTreeRef) {
        this.inputTreeRef = inputTreeRef;
        return this;
    }

    @JsonProperty("desc")
    public String getDesc() {
        return desc;
    }

    @JsonProperty("desc")
    public void setDesc(String desc) {
        this.desc = desc;
    }

    public ViewTreeInput withDesc(String desc) {
        this.desc = desc;
        return this;
    }

    @JsonProperty("show_genome_obj_name")
    public Long getShowGenomeObjName() {
        return showGenomeObjName;
    }

    @JsonProperty("show_genome_obj_name")
    public void setShowGenomeObjName(Long showGenomeObjName) {
        this.showGenomeObjName = showGenomeObjName;
    }

    public ViewTreeInput withShowGenomeObjName(Long showGenomeObjName) {
        this.showGenomeObjName = showGenomeObjName;
        return this;
    }

    @JsonProperty("color_for_reference_genomes")
    public String getColorForReferenceGenomes() {
        return colorForReferenceGenomes;
    }

    @JsonProperty("color_for_reference_genomes")
    public void setColorForReferenceGenomes(String colorForReferenceGenomes) {
        this.colorForReferenceGenomes = colorForReferenceGenomes;
    }

    public ViewTreeInput withColorForReferenceGenomes(String colorForReferenceGenomes) {
        this.colorForReferenceGenomes = colorForReferenceGenomes;
        return this;
    }

    @JsonProperty("color_for_skeleton_genomes")
    public String getColorForSkeletonGenomes() {
        return colorForSkeletonGenomes;
    }

    @JsonProperty("color_for_skeleton_genomes")
    public void setColorForSkeletonGenomes(String colorForSkeletonGenomes) {
        this.colorForSkeletonGenomes = colorForSkeletonGenomes;
    }

    public ViewTreeInput withColorForSkeletonGenomes(String colorForSkeletonGenomes) {
        this.colorForSkeletonGenomes = colorForSkeletonGenomes;
        return this;
    }

    @JsonProperty("color_for_user_genomes")
    public String getColorForUserGenomes() {
        return colorForUserGenomes;
    }

    @JsonProperty("color_for_user_genomes")
    public void setColorForUserGenomes(String colorForUserGenomes) {
        this.colorForUserGenomes = colorForUserGenomes;
    }

    public ViewTreeInput withColorForUserGenomes(String colorForUserGenomes) {
        this.colorForUserGenomes = colorForUserGenomes;
        return this;
    }

    @JsonProperty("tree_shape")
    public String getTreeShape() {
        return treeShape;
    }

    @JsonProperty("tree_shape")
    public void setTreeShape(String treeShape) {
        this.treeShape = treeShape;
    }

    public ViewTreeInput withTreeShape(String treeShape) {
        this.treeShape = treeShape;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((((((((((((((("ViewTreeInput"+" [workspaceName=")+ workspaceName)+", inputTreeRef=")+ inputTreeRef)+", desc=")+ desc)+", showGenomeObjName=")+ showGenomeObjName)+", colorForReferenceGenomes=")+ colorForReferenceGenomes)+", colorForSkeletonGenomes=")+ colorForSkeletonGenomes)+", colorForUserGenomes=")+ colorForUserGenomes)+", treeShape=")+ treeShape)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
