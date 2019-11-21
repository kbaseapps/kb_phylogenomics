
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
    "genome_disp_name_config",
    "show_skeleton_genome_sci_name",
    "reference_genome_disp",
    "skeleton_genome_disp",
    "user_genome_disp",
    "color_for_reference_genomes",
    "color_for_skeleton_genomes",
    "color_for_user_genomes",
    "tree_shape"
})
public class ViewTreeInput {

    @JsonProperty("workspace_name")
    private java.lang.String workspaceName;
    @JsonProperty("input_tree_ref")
    private java.lang.String inputTreeRef;
    @JsonProperty("desc")
    private java.lang.String desc;
    @JsonProperty("genome_disp_name_config")
    private java.lang.String genomeDispNameConfig;
    @JsonProperty("show_skeleton_genome_sci_name")
    private Long showSkeletonGenomeSciName;
    @JsonProperty("reference_genome_disp")
    private Map<String, Map<String, String>> referenceGenomeDisp;
    @JsonProperty("skeleton_genome_disp")
    private Map<String, Map<String, String>> skeletonGenomeDisp;
    @JsonProperty("user_genome_disp")
    private Map<String, Map<String, String>> userGenomeDisp;
    @JsonProperty("color_for_reference_genomes")
    private java.lang.String colorForReferenceGenomes;
    @JsonProperty("color_for_skeleton_genomes")
    private java.lang.String colorForSkeletonGenomes;
    @JsonProperty("color_for_user_genomes")
    private java.lang.String colorForUserGenomes;
    @JsonProperty("tree_shape")
    private java.lang.String treeShape;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("workspace_name")
    public java.lang.String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(java.lang.String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public ViewTreeInput withWorkspaceName(java.lang.String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("input_tree_ref")
    public java.lang.String getInputTreeRef() {
        return inputTreeRef;
    }

    @JsonProperty("input_tree_ref")
    public void setInputTreeRef(java.lang.String inputTreeRef) {
        this.inputTreeRef = inputTreeRef;
    }

    public ViewTreeInput withInputTreeRef(java.lang.String inputTreeRef) {
        this.inputTreeRef = inputTreeRef;
        return this;
    }

    @JsonProperty("desc")
    public java.lang.String getDesc() {
        return desc;
    }

    @JsonProperty("desc")
    public void setDesc(java.lang.String desc) {
        this.desc = desc;
    }

    public ViewTreeInput withDesc(java.lang.String desc) {
        this.desc = desc;
        return this;
    }

    @JsonProperty("genome_disp_name_config")
    public java.lang.String getGenomeDispNameConfig() {
        return genomeDispNameConfig;
    }

    @JsonProperty("genome_disp_name_config")
    public void setGenomeDispNameConfig(java.lang.String genomeDispNameConfig) {
        this.genomeDispNameConfig = genomeDispNameConfig;
    }

    public ViewTreeInput withGenomeDispNameConfig(java.lang.String genomeDispNameConfig) {
        this.genomeDispNameConfig = genomeDispNameConfig;
        return this;
    }

    @JsonProperty("show_skeleton_genome_sci_name")
    public Long getShowSkeletonGenomeSciName() {
        return showSkeletonGenomeSciName;
    }

    @JsonProperty("show_skeleton_genome_sci_name")
    public void setShowSkeletonGenomeSciName(Long showSkeletonGenomeSciName) {
        this.showSkeletonGenomeSciName = showSkeletonGenomeSciName;
    }

    public ViewTreeInput withShowSkeletonGenomeSciName(Long showSkeletonGenomeSciName) {
        this.showSkeletonGenomeSciName = showSkeletonGenomeSciName;
        return this;
    }

    @JsonProperty("reference_genome_disp")
    public Map<String, Map<String, String>> getReferenceGenomeDisp() {
        return referenceGenomeDisp;
    }

    @JsonProperty("reference_genome_disp")
    public void setReferenceGenomeDisp(Map<String, Map<String, String>> referenceGenomeDisp) {
        this.referenceGenomeDisp = referenceGenomeDisp;
    }

    public ViewTreeInput withReferenceGenomeDisp(Map<String, Map<String, String>> referenceGenomeDisp) {
        this.referenceGenomeDisp = referenceGenomeDisp;
        return this;
    }

    @JsonProperty("skeleton_genome_disp")
    public Map<String, Map<String, String>> getSkeletonGenomeDisp() {
        return skeletonGenomeDisp;
    }

    @JsonProperty("skeleton_genome_disp")
    public void setSkeletonGenomeDisp(Map<String, Map<String, String>> skeletonGenomeDisp) {
        this.skeletonGenomeDisp = skeletonGenomeDisp;
    }

    public ViewTreeInput withSkeletonGenomeDisp(Map<String, Map<String, String>> skeletonGenomeDisp) {
        this.skeletonGenomeDisp = skeletonGenomeDisp;
        return this;
    }

    @JsonProperty("user_genome_disp")
    public Map<String, Map<String, String>> getUserGenomeDisp() {
        return userGenomeDisp;
    }

    @JsonProperty("user_genome_disp")
    public void setUserGenomeDisp(Map<String, Map<String, String>> userGenomeDisp) {
        this.userGenomeDisp = userGenomeDisp;
    }

    public ViewTreeInput withUserGenomeDisp(Map<String, Map<String, String>> userGenomeDisp) {
        this.userGenomeDisp = userGenomeDisp;
        return this;
    }

    @JsonProperty("color_for_reference_genomes")
    public java.lang.String getColorForReferenceGenomes() {
        return colorForReferenceGenomes;
    }

    @JsonProperty("color_for_reference_genomes")
    public void setColorForReferenceGenomes(java.lang.String colorForReferenceGenomes) {
        this.colorForReferenceGenomes = colorForReferenceGenomes;
    }

    public ViewTreeInput withColorForReferenceGenomes(java.lang.String colorForReferenceGenomes) {
        this.colorForReferenceGenomes = colorForReferenceGenomes;
        return this;
    }

    @JsonProperty("color_for_skeleton_genomes")
    public java.lang.String getColorForSkeletonGenomes() {
        return colorForSkeletonGenomes;
    }

    @JsonProperty("color_for_skeleton_genomes")
    public void setColorForSkeletonGenomes(java.lang.String colorForSkeletonGenomes) {
        this.colorForSkeletonGenomes = colorForSkeletonGenomes;
    }

    public ViewTreeInput withColorForSkeletonGenomes(java.lang.String colorForSkeletonGenomes) {
        this.colorForSkeletonGenomes = colorForSkeletonGenomes;
        return this;
    }

    @JsonProperty("color_for_user_genomes")
    public java.lang.String getColorForUserGenomes() {
        return colorForUserGenomes;
    }

    @JsonProperty("color_for_user_genomes")
    public void setColorForUserGenomes(java.lang.String colorForUserGenomes) {
        this.colorForUserGenomes = colorForUserGenomes;
    }

    public ViewTreeInput withColorForUserGenomes(java.lang.String colorForUserGenomes) {
        this.colorForUserGenomes = colorForUserGenomes;
        return this;
    }

    @JsonProperty("tree_shape")
    public java.lang.String getTreeShape() {
        return treeShape;
    }

    @JsonProperty("tree_shape")
    public void setTreeShape(java.lang.String treeShape) {
        this.treeShape = treeShape;
    }

    public ViewTreeInput withTreeShape(java.lang.String treeShape) {
        this.treeShape = treeShape;
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
        return ((((((((((((((((((((((((((("ViewTreeInput"+" [workspaceName=")+ workspaceName)+", inputTreeRef=")+ inputTreeRef)+", desc=")+ desc)+", genomeDispNameConfig=")+ genomeDispNameConfig)+", showSkeletonGenomeSciName=")+ showSkeletonGenomeSciName)+", referenceGenomeDisp=")+ referenceGenomeDisp)+", skeletonGenomeDisp=")+ skeletonGenomeDisp)+", userGenomeDisp=")+ userGenomeDisp)+", colorForReferenceGenomes=")+ colorForReferenceGenomes)+", colorForSkeletonGenomes=")+ colorForSkeletonGenomes)+", colorForUserGenomes=")+ colorForUserGenomes)+", treeShape=")+ treeShape)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
